import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import math
import sys
sys.path.append('../MultiPropReg')
sys.path.append('./MultiPropReg')
import MultiPropReg.torch.layers as layers
from collections import namedtuple
from MultiPropReg.torch.operations import OPS
from torch.autograd import Variable
from MultiPropReg.torch.genotypes import *
from MultiPropReg.torch.layers import *
from MultiPropReg.torch.networks import *

# Set data shape
shape = (160, 192, 224)

class DeformableNet(nn.Module):
    
    def __init__(self, criterion, feature_operations, estimator_operations, hyper_1=10, hyper_2=15, hyper_3=3.2, hyper_4=0.8):
        super(DeformableNet, self).__init__()
        self.hyper_1 = hyper_1
        self.hyper_2 = hyper_2
        self.hyper_3 = hyper_3
        self.hyper_4 = hyper_4
        self.feature_operations = feature_operations
        self.estimator_operations = estimator_operations
        int_steps = 7
        inshape = shape
        down_shape2 = [int(d / 4) for d in inshape]
        down_shape1 = [int(d / 2) for d in inshape]
        self.criterion = criterion
        self.spatial_transform_f = layers.SpatialTransformer(volsize=down_shape1)
        self.spatial_transform = layers.SpatialTransformer(volsize=shape)

        # FeatureLearning/Encoder functions
        dim = 3
        self.enc = nn.ModuleList()
        self.enc.append(conv_block(dim, 1, 16, 2))  # 0 
        self.enc.append(conv_block(dim, 16, 16, 1))  # 1
        self.enc.append(conv_block(dim, 16, 16, 1))  # 2
        self.enc.append(conv_block(dim, 16, 32, 2))  # 3
        self.enc.append(conv_block(dim, 32, 32, 1))  # 4
        self.enc.append(conv_block(dim, 32, 32, 1))  # 5


        # Dncoder functions
        od = 32 + 1
        self.conv2_0 = conv_block(dim, od, 48, 1)  # [48, 32, 16]
        self.enc.append(self.conv2_0)
        self.conv2_1 = conv_block(dim, 48, 32, 1)
        self.enc.append(self.conv2_1)
        self.conv2_2 = conv_block(dim, 32, 16, 1)
        self.enc.append(self.conv2_2)
        self.predict_flow2a = predict_flow(16)
        self.enc.append(self.predict_flow2a)

        self.dc_conv2_0 = conv(3, 48, kernel_size=3, stride=1, padding=1, dilation=1) # [48, 48, 32]
        self.enc.append(self.dc_conv2_0)
        self.dc_conv2_1 = conv(48, 48, kernel_size=3, stride=1, padding=2, dilation=2)
        self.enc.append(self.dc_conv2_1)
        self.dc_conv2_2 = conv(48, 32, kernel_size=3, stride=1, padding=4, dilation=4)
        self.enc.append(self.dc_conv2_2)
        self.predict_flow2b = predict_flow(32)
        self.enc.append(self.predict_flow2b)

        od = 1 + 16 + 16 + 3
        self.conv1_0 = conv_block(dim, od, 48, 1)
        self.enc.append(self.conv1_0)
        self.conv1_1 = conv_block(dim, 48, 32, 1)
        self.enc.append(self.conv1_1)
        self.conv1_2 = conv_block(dim, 32, 16, 1)
        self.enc.append(self.conv1_2)
        self.predict_flow1a = predict_flow(16)
        self.enc.append(self.predict_flow1a)

        self.dc_conv1_0 = conv(3, 48, kernel_size=3, stride=1, padding=1, dilation=1)
        self.enc.append(self.dc_conv1_0)
        self.dc_conv1_1 = conv(48, 48, kernel_size=3, stride=1, padding=2, dilation=2)
        self.enc.append(self.dc_conv1_1)
        self.dc_conv1_2 = conv(48, 32, kernel_size=3, stride=1, padding=4, dilation=4)
        self.enc.append(self.dc_conv1_2)
        self.predict_flow1b = predict_flow(32)
        self.enc.append(self.predict_flow1b)

        self.resize = layers.ResizeTransform(1 / 2, dim)
        self.integrate2 = layers.VecInt(down_shape2, int_steps)
        self.integrate1 = layers.VecInt(down_shape1, int_steps)

    def forward(self, src, tgt):
        ##################### Feature extraction #########################
        c11 = self.enc[2](self.enc[1](self.enc[0](src)))
        c21 = self.enc[2](self.enc[1](self.enc[0](tgt)))
        c12 = self.enc[5](self.enc[4](self.enc[3](c11)))
        c22 = self.enc[5](self.enc[4](self.enc[3](c21)))

        ##################### Estimation at scale-2 #######################
        corr2 = MatchCost(c22, c12)
        x = torch.cat((corr2, c22), 1)
        x = self.conv2_0(x)
        x = self.conv2_1(x)
        x = self.conv2_2(x)
        flow2 = self.predict_flow2a(x)
        upfeat2 = self.resize(x)

        x = self.dc_conv2_0(flow2)
        x = self.dc_conv2_1(x)
        x = self.dc_conv2_2(x)
        refine_flow2 = self.predict_flow2b(x) + flow2
        int_flow2 = self.integrate2(refine_flow2)
        up_int_flow2 = self.resize(int_flow2)
        features_s_warped = self.spatial_transform_f(c11, up_int_flow2)

        ##################### Estimation at scale-1 #######################
        corr1 = MatchCost(c21, features_s_warped)
        x = torch.cat((corr1, c21, up_int_flow2, upfeat2), 1)
        x = self.conv1_0(x)
        x = self.conv1_1(x)
        x = self.conv1_2(x)
        flow1 = self.predict_flow1a(x) + up_int_flow2

        x = self.dc_conv1_0(flow1)
        x = self.dc_conv1_1(x)
        x = self.dc_conv1_2(x)
        refine_flow1 = self.predict_flow1b(x) + flow1
        int_flow1 = self.integrate1(refine_flow1)

        ##################### Upsample to scale-0 #######################
        flow = self.resize(int_flow1)
        y = self.spatial_transform(src, flow)

        return y, flow, flow1, refine_flow1, flow2, refine_flow2

    def _loss(self, src, tgt):
        y, flow, flow1, refine_flow1, flow2, refine_flow2 = self.forward(src, tgt)
        return self.criterion(y, tgt, src, flow, flow1, refine_flow1, flow2, refine_flow2,
                              self.hyper_1, self.hyper_2, self.hyper_3, self.hyper_4)

class Feature_learning(nn.Module):

    def __init__(self,PRIMITIVES):
        super(Feature_learning, self).__init__()

        self.enc_2 = nn.ModuleList()
        self.enc_1 = nn.ModuleList()

        self.enc_2.append(Cell_Op(16, 32, 2))  # 2层 (in_channels, out_channels, stride=1)
        self.enc_2.append(Cell_Op(32, 32, 1))  # 2层
        self.enc_2.append(Cell_Op(32, 32, 1))  # 2层

        self.enc_1.append(Cell_Op(1, 16, 2))  # 1层
        self.enc_1.append(Cell_Op(16, 16, 1))  # 1层
        self.enc_1.append(Cell_Op(16, 16, 1))  # 1层

    def forward(self, src, tgt, weights):
        c11 = self.enc_1[2](self.enc_1[1](self.enc_1[0](src, weights[0]), weights[1]), weights[2])
        c21 = self.enc_1[2](self.enc_1[1](self.enc_1[0](tgt, weights[0]), weights[1]), weights[2])
        c12 = self.enc_2[2](self.enc_2[1](self.enc_2[0](c11, weights[3]), weights[4]), weights[5])
        c22 = self.enc_2[2](self.enc_2[1](self.enc_2[0](c21, weights[3]), weights[4]), weights[5])
        s0, t0, s1, t1 = c11, c21, c12, c22
        return s0, t0, s1, t1


class MPR_net_Hyper(nn.Module):

    def __init__(self, criterion):
        super(MPR_net_Hyper, self).__init__()
        dim = 3
        int_steps = 7
        inshape = shape
        down_shape2 = [int(d / 4) for d in inshape]
        down_shape1 = [int(d / 2) for d in inshape]
        self.criterion = criterion
        self.spatial_transform_f = layers. SpatialTransformer(volsize=down_shape1)
        self.spatial_transform = layers.SpatialTransformer()

        # FeatureLearning/Encoder functions
        dim = 3
        self.enc = nn.ModuleList()
        self.enc.append(conv_block(dim, 1, 16, 2))  # 0 
        self.enc.append(conv_block(dim, 16, 16, 1))  # 1
        self.enc.append(conv_block(dim, 16, 16, 1))  # 2
        self.enc.append(conv_block(dim, 16, 32, 2))  # 3
        self.enc.append(conv_block(dim, 32, 32, 1))  # 4
        self.enc.append(conv_block(dim, 32, 32, 1))  # 5

        od = 32 + 1
        self.conv2_0 = conv_block(dim, od, 48, 1) 
        self.enc.append(self.conv2_0)
        self.conv2_1 = conv_block(dim, 48, 32, 1)
        self.enc.append(self.conv2_1)
        self.conv2_2 = conv_block(dim, 32, 16, 1)
        self.enc.append(self.conv2_2)
        self.predict_flow2a = predict_flow(16)
        self.enc.append(self.predict_flow2a)

        self.dc_conv2_0 = conv(3, 48, kernel_size=3, stride=1, padding=1, dilation=1) 
        self.enc.append(self.dc_conv2_0)
        self.dc_conv2_1 = conv(48, 48, kernel_size=3, stride=1, padding=2, dilation=2)
        self.enc.append(self.dc_conv2_1)
        self.dc_conv2_2 = conv(48, 32, kernel_size=3, stride=1, padding=4, dilation=4)
        self.enc.append(self.dc_conv2_2)
        self.predict_flow2b = predict_flow(32)
        self.enc.append(self.predict_flow2b)

        od = 1 + 16 + 16 + 3
        self.conv1_0 = conv_block(dim, od, 48, 1)
        self.enc.append(self.conv1_0)
        self.conv1_1 = conv_block(dim, 48, 32, 1)
        self.enc.append(self.conv1_1)
        self.conv1_2 = conv_block(dim, 32, 16, 1)
        self.enc.append(self.conv1_2)
        self.predict_flow1a = predict_flow(16)
        self.enc.append(self.predict_flow1a)

        self.dc_conv1_0 = conv(3, 48, kernel_size=3, stride=1, padding=1, dilation=1)
        self.enc.append(self.dc_conv1_0)
        self.dc_conv1_1 = conv(48, 48, kernel_size=3, stride=1, padding=2, dilation=2)
        self.enc.append(self.dc_conv1_1)
        self.dc_conv1_2 = conv(48, 32, kernel_size=3, stride=1, padding=4, dilation=4)
        self.enc.append(self.dc_conv1_2)
        self.predict_flow1b = predict_flow(32)
        self.enc.append(self.predict_flow1b)


        self.resize = layers.ResizeTransform(1 / 2, dim)

        self.integrate2 = layers.VecInt(down_shape2, int_steps)
        self.integrate1 = layers.VecInt(down_shape1, int_steps)
        self.hyper_1 = torch.nn.Parameter(torch.FloatTensor(1), requires_grad=True)
        self.hyper_2 = torch.nn.Parameter(torch.FloatTensor(1), requires_grad=True)
        self.hyper_3 = torch.nn.Parameter(torch.FloatTensor(1), requires_grad=True)
        self.hyper_4 = torch.nn.Parameter(torch.FloatTensor(1), requires_grad=True)

        # 初始化
        self.hyper_1.data.fill_(10)
        self.hyper_2.data.fill_(15)
        self.hyper_3.data.fill_(3.2)
        self.hyper_4.data.fill_(0.8)

    def forward(self, src, tgt):

        c11 = self.enc[2](self.enc[1](self.enc[0](src)))
        c21 = self.enc[2](self.enc[1](self.enc[0](tgt)))
        c12 = self.enc[5](self.enc[4](self.enc[3](c11)))
        c22 = self.enc[5](self.enc[4](self.enc[3](c21)))

        corr2 = MatchCost(c22, c12)
        x = torch.cat((corr2, c22), 1)
        x = self.conv2_0(x)
        x = self.conv2_1(x)
        x = self.conv2_2(x)
        flow2 = self.predict_flow2a(x)
        upfeat2 = self.resize(x)

        x = self.dc_conv2_0(flow2)
        x = self.dc_conv2_1(x)
        x = self.dc_conv2_2(x)
        refine_flow2 = self.predict_flow2b(x) + flow2
        int_flow2 = self.integrate2(refine_flow2)
        up_int_flow2 = self.resize(int_flow2)
        features_s_warped = self.spatial_transform_f(c11, up_int_flow2)


        corr1 = MatchCost(c21, features_s_warped)
        x = torch.cat((corr1, c21, up_int_flow2, upfeat2), 1)
        x = self.conv1_0(x)
        x = self.conv1_1(x)
        x = self.conv1_2(x)
        flow1 = self.predict_flow1a(x) + up_int_flow2

        x = self.dc_conv1_0(flow1)
        x = self.dc_conv1_1(x)
        x = self.dc_conv1_2(x)
        refine_flow1 = self.predict_flow1b(x) + flow1
        int_flow1 = self.integrate1(refine_flow1)
        flow = self.resize(int_flow1)
        y = self.spatial_transform(src, flow)
        return y, flow, int_flow1, refine_flow1, int_flow2, refine_flow2

    def hyper_parameters(self):
        return [self.hyper_1, self.hyper_2, self.hyper_3, self.hyper_4]

    def y_parameters(self):
        return self.parameters()

    def _loss(self, src, tgt):
        y, flow, flow1, refine_flow1, flow2, refine_flow2 = self.forward(src, tgt)
        return self.criterion(y, tgt, src, flow, flow1, refine_flow1, flow2, refine_flow2,
                              self.hyper_1, self.hyper_2, self.hyper_3, self.hyper_4)

    def new(self):
        model_new = MPR_net_Hyper(self.criterion).cuda()
        for x, y in zip(model_new.hyper_parameters(), self.hyper_parameters()):
            x.data.copy_(y.data)
        return model_new


class MPR_net_noHyper(nn.Module):

    def __init__(self, criterion):
        super(MPR_net_noHyper, self).__init__()
        dim = 3
        int_steps = 7
        inshape = shape
        down_shape2 = [int(d / 4) for d in inshape]
        down_shape1 = [int(d / 2) for d in inshape]
        self.criterion = criterion
        self.spatial_transform_f = layers.SpatialTransformer(volsize=down_shape1) 
        self.spatial_transform = layers.SpatialTransformer(volsize=shape)

        # FeatureLearning/Encoder functions
        dim = 3
        self.enc = nn.ModuleList()
        self.enc.append(conv_block(dim, 1, 16, 2))  # 0 
        self.enc.append(conv_block(dim, 16, 16, 1))  # 1
        self.enc.append(conv_block(dim, 16, 16, 1))  # 2
        self.enc.append(conv_block(dim, 16, 32, 2))  # 3
        self.enc.append(conv_block(dim, 32, 32, 1))  # 4
        self.enc.append(conv_block(dim, 32, 32, 1))  # 5

        od = 32 + 1
        self.conv2_0 = conv_block(dim, od, 48, 1) # [48, 32, 16]
        self.enc.append(self.conv2_0)
        self.conv2_1 = conv_block(dim, 48, 32, 1)
        self.enc.append(self.conv2_1)
        self.conv2_2 = conv_block(dim, 32, 16, 1)
        self.enc.append(self.conv2_2)
        self.predict_flow2a = predict_flow(16)
        self.enc.append(self.predict_flow2a)

        self.dc_conv2_0 = conv(3, 48, kernel_size=3, stride=1, padding=1, dilation=1) # [48, 48, 32]
        self.enc.append(self.dc_conv2_0)
        self.dc_conv2_1 = conv(48, 48, kernel_size=3, stride=1, padding=2, dilation=2)
        self.enc.append(self.dc_conv2_1)
        self.dc_conv2_2 = conv(48, 32, kernel_size=3, stride=1, padding=4, dilation=4)
        self.enc.append(self.dc_conv2_2)
        self.predict_flow2b = predict_flow(32)
        self.enc.append(self.predict_flow2b)

        od = 1 + 16 + 16 + 3
        self.conv1_0 = conv_block(dim, od, 48, 1)
        self.enc.append(self.conv1_0)
        self.conv1_1 = conv_block(dim, 48, 32, 1)
        self.enc.append(self.conv1_1)
        self.conv1_2 = conv_block(dim, 32, 16, 1)
        self.enc.append(self.conv1_2)
        self.predict_flow1a = predict_flow(16)
        self.enc.append(self.predict_flow1a)

        self.dc_conv1_0 = conv(3, 48, kernel_size=3, stride=1, padding=1, dilation=1)
        self.enc.append(self.dc_conv1_0)
        self.dc_conv1_1 = conv(48, 48, kernel_size=3, stride=1, padding=2, dilation=2)
        self.enc.append(self.dc_conv1_1)
        self.dc_conv1_2 = conv(48, 32, kernel_size=3, stride=1, padding=4, dilation=4)
        self.enc.append(self.dc_conv1_2)
        self.predict_flow1b = predict_flow(32)
        self.enc.append(self.predict_flow1b)


        self.resize = layers.ResizeTransform(1 / 2, dim)

        self.integrate2 = layers.VecInt(down_shape2, int_steps)
        self.integrate1 = layers.VecInt(down_shape1, int_steps)


    def forward(self, src, tgt):

        c11 = self.enc[2](self.enc[1](self.enc[0](src)))
        c21 = self.enc[2](self.enc[1](self.enc[0](tgt)))
        c12 = self.enc[5](self.enc[4](self.enc[3](c11)))
        c22 = self.enc[5](self.enc[4](self.enc[3](c21)))

        corr2 = MatchCost(c22, c12)
        x = torch.cat((corr2, c22), 1)
        x = self.conv2_0(x)
        x = self.conv2_1(x)
        x = self.conv2_2(x)
        flow2 = self.predict_flow2a(x)
        upfeat2 = self.resize(x)

        x = self.dc_conv2_0(flow2)
        x = self.dc_conv2_1(x)
        x = self.dc_conv2_2(x)
        refine_flow2 = self.predict_flow2b(x) + flow2
        int_flow2 = self.integrate2(refine_flow2)
        up_int_flow2 = self.resize(int_flow2)
        features_s_warped = self.spatial_transform_f(c11, up_int_flow2)


        corr1 = MatchCost(c21, features_s_warped)
        x = torch.cat((corr1, c21, up_int_flow2, upfeat2), 1)
        x = self.conv1_0(x)
        x = self.conv1_1(x)
        x = self.conv1_2(x)
        flow1 = self.predict_flow1a(x) + up_int_flow2

        x = self.dc_conv1_0(flow1)
        x = self.dc_conv1_1(x)
        x = self.dc_conv1_2(x)
        refine_flow1 = self.predict_flow1b(x) + flow1
        int_flow1 = self.integrate1(refine_flow1)
        flow = self.resize(int_flow1)
        y = self.spatial_transform(src, flow)
        return y, flow, int_flow1, int_flow2

    def y_parameters(self):
        return self.parameters()

    def _loss(self, src, tgt):
        y, flow, flow1, flow2 = self.forward(src, tgt)
        return self.criterion(y, tgt, src, flow, flow1, flow2, 10, 15, 3.2, 0.8)

    def new(self):
        model_new = MPR_net_Hyper(self.criterion).cuda()
        for x, y in zip(model_new.hyper_parameters(), self.hyper_parameters()):
            x.data.copy_(y.data)
        return model_new


class ReLUConvBN(nn.Module):
    def __init__(self, C_in, C_out, kernel_size, stride, padding):
        super(ReLUConvBN, self).__init__()
        self.op = nn.Sequential(
            nn.Conv3d(C_in, C_out, kernel_size, stride=stride, padding=padding, bias=False),
            nn.LeakyReLU(0.2))
    def forward(self, x):
        return self.op(x)


class DilConv(nn.Module):
    def __init__(self, C_in, C_out, kernel_size, stride, padding, dilation):
        super(DilConv, self).__init__()
        self.op = nn.Sequential(
            nn.Conv3d(C_in, C_out, kernel_size, stride=stride, padding=padding, dilation=dilation),
            nn.LeakyReLU(0.2))
    def forward(self, x):
        return self.op(x)


class SepConv(nn.Module):
    def __init__(self, C_in, C_out, kernel_size, stride, padding):
        super(SepConv, self).__init__()
        self.op = nn.Sequential(
            nn.Conv3d(C_in, C_in, kernel_size, stride=1, padding=padding, bias=False),
            nn.LeakyReLU(0.2),
            nn.Conv3d(C_in, C_in, kernel_size=kernel_size, stride=stride, padding=padding, groups=C_in, bias=False),
            nn.Conv3d(C_in, C_out, kernel_size=1, padding=0, bias=False),
            nn.LeakyReLU(0.2)
        )
    def forward(self, x):
        return self.op(x)

OPS = {
    'conv_1x1': lambda C_in, C_out, stride: ReLUConvBN(C_in, C_out, 1, stride, 0),
    'conv_3x3': lambda C_in, C_out, stride: ReLUConvBN(C_in, C_out, 3, stride, 1),
    'conv_5x5': lambda C_in, C_out, stride: ReLUConvBN(C_in, C_out, 5, stride, 2),
    'sep_conv_3x3': lambda C_in, C_out, stride: SepConv(C_in, C_out, 3, stride, 1),
    'sep_conv_5x5': lambda C_in, C_out, stride: SepConv(C_in, C_out, 5, stride, 2),
    'dil_conv_3x3': lambda C_in, C_out, stride: DilConv(C_in, C_out, 3, stride, 2, 2),
    'dil_conv_5x5': lambda C_in, C_out, stride: DilConv(C_in, C_out, 5, stride, 4, 2),
    'dil_conv_7x7': lambda C_in, C_out, stride: DilConv(C_in, C_out, 7, stride, 6, 2),
    'dil_conv_3x3_8': lambda C_in, C_out, stride: DilConv(C_in, C_out, 3, stride, 8, 8), 
}

class ModelCell(nn.Module):
  def __init__(self, primitive, in_channels, out_channels, stride=1):
    super(ModelCell, self).__init__()

    self.op = OPS[primitive](in_channels, out_channels, stride)

  def forward(self, x):
    return self.op(x)

class Concat_Cell(nn.Module):

    def __init__(self, genotype):
        super(Concat_Cell, self).__init__()
        self.genotype = genotype

        self.enc_2 = nn.ModuleList()
        self.enc_1 = nn.ModuleList()

        self.enc_2.append(ModelCell(self.genotype[3], 64, 48, 1))  # 2�� (in_channels, out_channels, stride=1)
        self.enc_2.append(ModelCell(self.genotype[4], 48, 32, 1))  # 2��
        self.enc_2.append(ModelCell(self.genotype[5], 32, 16, 1))  # 2��

        self.enc_1.append(ModelCell(self.genotype[0], 51, 48, 1))  # 1��
        self.enc_1.append(ModelCell(self.genotype[1], 48, 32, 1))  # 1��
        self.enc_1.append(ModelCell(self.genotype[2], 32, 16, 1))  # 1��

    def forward(self, src, tgt, up_int_flow, upfeat):

        input_list = list(src.size())
        channel = int(input_list[1])
        if channel == 16:
            x = torch.cat((src, tgt, up_int_flow, upfeat), 1)
            x = self.enc_1[2](self.enc_1[1](self.enc_1[0](x)))
        elif channel == 32:
            x = torch.cat((src, tgt), 1)
            x = self.enc_2[2](self.enc_2[1](self.enc_2[0](x)))
        return x

class FeatureExtraction(nn.Module):
    def __init__(self, operations):
        super(FeatureExtraction, self).__init__()
        self.operations = operations
        self.enc = nn.ModuleList()
        self.enc.append(ModelCell(self.operations[0], 1, 16, 2))  # 0 (in_channels, out_channels, stride=1)
        self.enc.append(ModelCell(self.operations[1], 16, 16, 1))  # 1
        self.enc.append(ModelCell(self.operations[2], 16, 16, 1))  # 2
        self.enc.append(ModelCell(self.operations[3], 16, 32, 2))  # 3
        self.enc.append(ModelCell(self.operations[4], 32, 32, 1))  # 4
        self.enc.append(ModelCell(self.operations[5], 32, 32, 1))  # 5

    def forward(self, src, tgt):
        c11 = self.enc[2](self.enc[1](self.enc[0](src)))
        c21 = self.enc[2](self.enc[1](self.enc[0](tgt)))
        c12 = self.enc[5](self.enc[4](self.enc[3](c11)))
        c22 = self.enc[5](self.enc[4](self.enc[3](c21)))
        s0, t0, s1, t1 = c11, c21, c12, c22
        return s0, t0, s1, t1

class Network_Search_Feature(nn.Module):
    def __init__(self, criterion, shape, operations):
        super(Network_Search_Feature, self).__init__()
        self._criterion = criterion
        self._shape = shape
        self._operations = operations
        self.enc = nn.ModuleList()
        self.enc.append(Cell(1, 16, 2))  # 0
        self.enc.append(Cell(16, 16, 1))  # 1
        self.enc.append(Cell(16, 16, 1))  # 2
        self.enc.append(Cell(16, 32, 2))  # 3
        self.enc.append(Cell(32, 32, 1))  # 4
        self.enc.append(Cell(32, 32, 1))  # 5

        self.estimator = Estimator(self._shape, self._operations)
        self._initialize_alphas()

    def forward(self, src, tgt):
        weights = F.softmax(self.alphas, dim=-1)
        c11 = self.enc[2](self.enc[1](self.enc[0](src, weights[0]), weights[1]), weights[2])    
        c12 = self.enc[5](self.enc[4](self.enc[3](c11, weights[3]), weights[4]), weights[5])

        c21 = self.enc[2](self.enc[1](self.enc[0](tgt, weights[0]), weights[1]), weights[2])
        c22 = self.enc[5](self.enc[4](self.enc[3](c21, weights[3]), weights[4]), weights[5])

        s0, t0, s1, t1 = c11, c21, c12, c22

        y, flow, int_flow1, refine_flow1, int_flow2, refine_flow2 = self.estimator(s0, t0, s1, t1, src)
        return y, flow, int_flow1, refine_flow1, int_flow2, refine_flow2 

    def new(self):
        model_new = Network_Search_Feature(self._criterion, self._shape).cuda()
        for x, y in zip(model_new.arch_parameters(), self.arch_parameters()):
            x.data.copy_(y.data)
        return model_new

    def _loss(self, src, tgt):
        y, flow, flow1, refine_flow1, flow2, refine_flow2 = self.forward(src, tgt)
        return self._criterion(y, tgt, src, flow, flow1, refine_flow1, flow2, refine_flow2)

    def _initialize_alphas(self):
            num_ops = len(PRIMITIVES)
            k_concat = 6
            self.alphas = Variable(1e-3 * torch.randn(k_concat, num_ops).cuda(), requires_grad=True)#Variable 没看懂
            self._arch_parameters = [
                self.alphas,
            ]
            
    def arch_parameters(self):
        return self._arch_parameters

    def genotype(self):
        def _parse(weights, k=6):
            gene = []
            for i in range(k):
                W = weights[i].copy()
                k_best = None
                for k in range(len(W)):
                    if k_best is None or W[k] > W[k_best]:
                        k_best = k
                gene.append((PRIMITIVES[k_best]))
            return gene
        gene = _parse(F.softmax(self.alphas, dim=-1).data.cpu().numpy())
        genotype = Genotype(arch=gene)
        return genotype
    
class Network_Search_Estimator(nn.Module):
    def __init__(self, criterion, cell_name, shape, operations):
        super(Network_Search_Estimator, self).__init__()
        self._criterion = criterion
        self._cellname = cell_name
        self._shape = shape
        self._operations = operations
        self.fea = FeatureExtraction(self._operations)
        self.cell = Cell_Operation[cell_name](PRIMITIVES)
        self._initialize_alphas()

        int_steps = 7
        down_shape2 = [int(d / 4) for d in self._shape]
        down_shape1 = [int(d / 2) for d in self._shape]
        self.resize = ResizeTransform(1 / 2, ndims=3)
        self.spatial_transform_f = SpatialTransformer(volsize=down_shape1)
        self.spatial_transform = SpatialTransformer(volsize=self._shape)
        self.predict_flow = predict_flow(16)
        self.integrate2 = VecInt(down_shape2, int_steps)
        self.integrate1 = VecInt(down_shape1, int_steps)
        self.integrate0 = VecInt(self._shape, int_steps)
        

    def forward(self, src, tgt):
        s0, t0, s1, t1 = self.fea(src, tgt)
        up_int_flow = None
        up_feat = None
        weights_alpha = F.softmax(self.alphas, dim=-1)
        f2 = self.cell(s1, t1, up_int_flow, up_feat, weights_alpha)
        flow2 = self.predict_flow(f2)
        upfeat2 = self.resize(f2)
        refine_flow2 = self.predict_flow(f2) + flow2
        int_flow2 = self.integrate2(refine_flow2)
        up_int_flow2 = self.resize(int_flow2)
        features_s_warped = self.spatial_transform_f(s0, up_int_flow2)

        f1 = self.cell(features_s_warped, t0, up_int_flow2, upfeat2, weights_alpha)
        flow1 = self.predict_flow(f1)
        refine_flow1 = self.predict_flow(f1) + flow1
        int_flow1 = self.integrate1(refine_flow1)

        flow = self.resize(int_flow1)
        flow = self.integrate0(flow)
        y = self.spatial_transform(src, flow)
        return y, flow, int_flow1, refine_flow1, int_flow2, refine_flow2

    def _loss(self, src, tgt):
        y, flow, flow1, refine_flow1, flow2, refine_flow2 = self.forward(src, tgt)
        return self._criterion(y, tgt, src, flow, flow1, refine_flow1, flow2, refine_flow2)

    def new(self):
        model_new = Network_Search_Estimator(self._criterion, self._cellname, self._shape).cuda()
        for x, y in zip(model_new.arch_parameters(), self.arch_parameters()):
            x.data.copy_(y.data)
        return model_new

    def _initialize_alphas(self):

        num_ops = len(PRIMITIVES)
        k_concat = 6
        self.alphas = Variable(1e-3 * torch.randn(k_concat, num_ops).cuda(), requires_grad=True)#Variable 没看懂
        self._arch_parameters = [
            self.alphas,
        ]

    def arch_parameters(self):
        return self._arch_parameters

    def genotype(self):
        def _parse(weights, k=6):
            gene = []
            for i in range(k):
                W = weights[i].copy()
                k_best = None
                for k in range(len(W)):
                    if k_best is None or W[k] > W[k_best]:
                        k_best = k
                gene.append((PRIMITIVES[k_best]))
            return gene

        gene = _parse(F.softmax(self.alphas, dim=-1).data.cpu().numpy())
        genotype = Genotype(arch=gene)
        return genotype
    
class Network_Search_all(nn.Module):
    def __init__(self,criterion, cell_name, shape):
        super(Network_Search_all, self).__init__()
        self._criterion = criterion
        self._cellname = cell_name
        self._shape = shape
        self.cell = Cell_Operation[cell_name](PRIMITIVES)
        self.fea = Feature_learning(PRIMITIVES)
        self._initialize_alphas()

        int_steps = 7

        down_shape2 = [int(d / 4) for d in self._shape]
        down_shape1 = [int(d / 2) for d in self._shape]
        self.resize = ResizeTransform(1 / 2, ndims=3)
        self.spatial_transform_f = SpatialTransformer(volsize=down_shape1)
        self.spatial_transform = SpatialTransformer(volsize=self._shape)
        self.predict_flow = predict_flow(16)
        self.integrate2 = VecInt(down_shape2, int_steps)
        self.integrate1 = VecInt(down_shape1, int_steps)
        self.integrate0 = VecInt(self._shape, int_steps)

    def forward(self, src, tgt):

        weights_fea = F.softmax(self.alphas_fea, dim=-1)
        s0, t0, s1, t1 = self.fea(src, tgt, weights_fea)
        up_int_flow = None
        up_feat = None
        weights_op = F.softmax(self.alphas_op, dim=-1)
        f2 = self.cell(s1, t1, up_int_flow, up_feat, weights_op)
        flow2 = self.predict_flow(f2)
        upfeat2 = self.resize(f2)
        refine_flow2 = self.predict_flow(f2) + flow2
        int_flow2 = self.integrate2(refine_flow2)
        up_int_flow2 = self.resize(int_flow2)
        features_s_warped = self.spatial_transform_f(s0, up_int_flow2)


        f1 = self.cell(features_s_warped, t0, up_int_flow2, upfeat2,weights_op)
        flow1 = self.predict_flow(f1)
        refine_flow1 = self.predict_flow(f1) + flow1
        int_flow1 = self.integrate1(refine_flow1)

        flow = self.resize(int_flow1)
        flow = self.integrate0(flow)
        y = self.spatial_transform(src, flow)
        return y, flow, int_flow1, refine_flow1, int_flow2, refine_flow2

    def _loss(self, src, tgt):
        y, flow, flow1, refine_flow1, flow2, refine_flow2 = self.forward(src, tgt)
        return self._criterion(y, tgt, src, flow, flow1, refine_flow1, flow2, refine_flow2)

    def new(self):
        model_new = Network_Search_all(self._criterion, self._cellname, self._shape).cuda()
        for x, y in zip(model_new.arch_parameters(), self.arch_parameters()):
            x.data.copy_(y.data)
        return model_new

    def _initialize_alphas(self):
        num_ops = len(PRIMITIVES)
        k_concat = 6
        self.alphas_fea = Variable(1e-3 * torch.randn(k_concat, num_ops).cuda(), requires_grad=True)
        self.alphas_op = Variable(1e-3 * torch.randn(k_concat, num_ops).cuda(), requires_grad=True)
        self._arch_parameters = [
            self.alphas_fea,
            self.alphas_op
        ]

    def arch_parameters(self):
        return self._arch_parameters

    def genotype(self):
        def _parse_fea(weights, k=6):
            gene = []
            for i in range(k):
                W = weights[i].copy()
                k_best = None
                for k in range(len(W)):
                    if k_best is None or W[k] > W[k_best]:
                        k_best = k
                gene.append((PRIMITIVES[k_best]))
            return gene

        def _parse_op(weights, k=6):
            gene = []
            for i in range(k):
                W = weights[i].copy()
                k_best = None
                for k in range(len(W)):
                    if k_best is None or W[k] > W[k_best]:
                        k_best = k
                gene.append((PRIMITIVES[k_best]))
            return gene

        gene_fea = _parse_fea(F.softmax(self.alphas_fea, dim=-1).data.cpu().numpy())
        gene_op = _parse_op(F.softmax(self.alphas_op, dim=-1).data.cpu().numpy())
        genotype = Genotype_all(normal_fea=gene_fea, normal_op=gene_op)
        return genotype

class Estimator(nn.Module):
    def __init__(self, shape, operations):
        super(Estimator, self).__init__()

        self.operations = operations
        genotype = operations
        self.cell = Concat_Cell(genotype)
        int_steps = 7

        down_shape2 = [int(d / 4) for d in shape]
        down_shape1 = [int(d / 2) for d in shape]
        self.resize = ResizeTransform(1 / 2, ndims=3)
        self.spatial_transform_f = SpatialTransformer(volsize=down_shape1)
        self.spatial_transform = SpatialTransformer(volsize=shape)
        self.predict_flow = predict_flow(16)
        self.integrate2 = VecInt(down_shape2, int_steps)
        self.integrate1 = VecInt(down_shape1, int_steps)
        self.integrate0 = VecInt(shape, int_steps)

    def forward(self, s0, t0, s1, t1, src):
        up_int_flow = None
        up_feat = None
        f2 = self.cell(s1, t1, up_int_flow, up_feat)
        flow2 = self.predict_flow(f2)
        upfeat2 = self.resize(f2)
        refine_flow2 = self.predict_flow(f2) + flow2
        int_flow2 = self.integrate2(refine_flow2)
        up_int_flow2 = self.resize(int_flow2)
        features_s_warped = self.spatial_transform_f(s0, up_int_flow2)

        f1 = self.cell(features_s_warped, t0, up_int_flow2, upfeat2)
        flow1 = self.predict_flow(f1)
        refine_flow1 = self.predict_flow(f1) + flow1
        int_flow1 = self.integrate1(refine_flow1)

        flow = self.resize(int_flow1)
        flow = self.integrate0(flow)
        y = self.spatial_transform(src, flow)
        return y, flow, int_flow1, refine_flow1, int_flow2, refine_flow2

class Deformable(nn.Module):

    def __init__(self, criterion, shape, feature_operations, estimator_operations):
        super(Deformable, self).__init__()
        self._criterion = criterion
        self._shape = shape
        self.feature_operations = feature_operations
        self.estimator_operations = estimator_operations
        self.FeatureExtraction = FeatureExtraction(self.feature_operations)
        self.Estimator = Estimator(self._shape, self.estimator_operations)
    def forward(self, src, tgt):
        s0, t0, s1, t1 = self.FeatureExtraction(src, tgt)
        y, flow, int_flow1, refine_flow1, int_flow2, refine_flow2 = self.Estimator(s0, t0, s1, t1, src)
        return y, flow, int_flow1, refine_flow1, int_flow2, refine_flow2
    def _loss(self, src, tgt):
        y, flow, flow1, refine_flow1, flow2, refine_flow2 = self.forward(src, tgt)
        return self._criterion(y, tgt, src, flow, flow1, refine_flow1, flow2, refine_flow2)


class MPR_net_Hyper1(nn.Module):

    def __init__(self, criterion, feature_operations, estimator_operations):
        super(MPR_net_Hyper1, self).__init__()
        self.feature_operations = feature_operations
        self.estimator_operations = estimator_operations
        self.Reg = Deformable(criterion, shape, self.feature_operations, self.estimator_operations)
        self.hyper_1 = torch.nn.Parameter(torch.FloatTensor(1), requires_grad=True)
        self.hyper_2 = torch.nn.Parameter(torch.FloatTensor(1), requires_grad=True)
        self.hyper_3 = torch.nn.Parameter(torch.FloatTensor(1), requires_grad=True)
        self.hyper_4 = torch.nn.Parameter(torch.FloatTensor(1), requires_grad=True)
        self.criterion = criterion

        # 初始化
        self.hyper_1.data.fill_(10)
        self.hyper_2.data.fill_(15)
        self.hyper_3.data.fill_(3.2)
        self.hyper_4.data.fill_(0.8)

    def forward(self, src, tgt):
      # y, flow, int_flow1, refine_flow1, int_flow2, refine_flow2 
    #   y, flow, flow1, refine_flow1, flow2, refine_flow2 = self.Reg(src, tgt)
      return self.Reg(src, tgt)
      

    def hyper_parameters(self):
        return [self.hyper_1, self.hyper_2, self.hyper_3, self.hyper_4]

    def y_parameters(self):
        return self.parameters()

    def _loss(self, src, tgt):
        y, flow, flow1, refine_flow1, flow2, refine_flow2 = self.forward(src, tgt)
        return self.criterion(y, tgt, src, flow, flow1, refine_flow1, flow2, refine_flow2,
                              self.hyper_1, self.hyper_2, self.hyper_3, self.hyper_4)

    def new(self):
        model_new = MPR_net_Hyper1(self.criterion, self.feature_operations, self.estimator_operations).cuda()
        for x, y in zip(model_new.hyper_parameters(), self.hyper_parameters()):
            x.data.copy_(y.data)
        return model_new
    
class MPR_net_noHyper1(nn.Module):

    def __init__(self, criterion, feature_operations, estimator_operations):
        super(MPR_net_noHyper1, self).__init__()
        self.feature_operations = feature_operations
        self.estimator_operations = estimator_operations
        self.Reg = Deformable(criterion, shape, self.feature_operations, self.estimator_operations)
        self.criterion = criterion

    def forward(self, src, tgt):
        # Assuming Reg returns y, flow, int_flow1, refine_flow1, int_flow2, refine_flow2
        return self.Reg(src, tgt)

    def _loss(self, src, tgt):
        y, flow, flow1, refine_flow1, flow2, refine_flow2 = self.forward(src, tgt)
        return self.criterion(y, tgt, src, flow, flow1, refine_flow1, flow2, refine_flow2)

    def new(self):
        model_new = MPR_net_noHyper1(self.criterion, self.feature_operations, self.estimator_operations).cuda()
        return model_new



class MPRNet_ST(nn.Module):

    def __init__(self, criterion_reg, criterion_seg, feature_operations, estimator_operations):
        super(MPRNet_ST, self).__init__()
        self.criterion_reg, self.criterion_seg = criterion_reg, criterion_seg
        self.feature_operations = feature_operations
        self.estimator_operations = estimator_operations

        self.Reg = self.Reg = Deformable(criterion_reg, shape, self.feature_operations, self.estimator_operations)
        self.hyper_1 = torch.nn.Parameter(torch.FloatTensor([10]), requires_grad=True) 
        self.hyper_2 = torch.nn.Parameter(torch.FloatTensor([15]), requires_grad=True)
        self.hyper_3 = torch.nn.Parameter(torch.FloatTensor([3.2]), requires_grad=True)
        self.hyper_4 = torch.nn.Parameter(torch.FloatTensor([0.8]), requires_grad=True)
        self.hyper_5 = torch.nn.Parameter(torch.FloatTensor([0.5]), requires_grad=True)

    def forward(self, tgt, src):
        y, flow, flow1, refine_flow1, flow2, refine_flow2 = self.Reg(tgt, src)
        return y, flow, flow1, refine_flow1, flow2, refine_flow2

    def upper_parameters(self):
        return [self.hyper_1, self.hyper_2, self.hyper_3, self.hyper_4, self.hyper_5]

    def lower_parameters(self): 
        return self.Reg.parameters()

    def _upper_loss(self, tgt, src, tgt_mask, src_mask):
        y, flow, flow1, refine_flow1, flow2, refine_flow2 = self(tgt, src)
        loss = self.criterion_seg(tgt_mask, src_mask, flow)
        return loss

    def _lower_loss(self, tgt, src):
        y, flow, flow1, refine_flow1, flow2, refine_flow2 = self(tgt, src) 
        loss = self.criterion_reg(y, tgt, src, flow, flow1, refine_flow1, flow2, refine_flow2, self.hyper_1, self.hyper_2, self.hyper_3, self.hyper_4, self.hyper_5)
        return loss

    def new(self):
        model_new = MPRNet_ST(self.criterion_reg, self.criterion_seg, self.feature_operations, self.estimator_operations).cuda()
        for x, y in zip(model_new.upper_parameters(), self.upper_parameters()):
            x.data.copy_(y.data)
        return model_new   

class MPRNet(nn.Module):

    def __init__(self):
        super(MPRNet, self).__init__()
        dim = 3
        int_steps = 7
        inshape = shape
        down_shape2 = [int(d / 4) for d in inshape]
        down_shape1 = [int(d / 2) for d in inshape]
        self.FeatureLearning = FeatureLearning()
        self.spatial_transform_f = SpatialTransformer(volsize=down_shape1)
        self.spatial_transform = SpatialTransformer()

        od = 32 + 1
        self.conv2_0 = conv_block(dim, od, 48, 1)
        self.conv2_1 = conv_block(dim, 48, 32, 1)
        self.conv2_2 = conv_block(dim, 32, 16, 1)
        self.predict_flow2a = predict_flow(16)

        self.dc_conv2_0 = conv(3, 48, kernel_size=3, stride=1, padding=1, dilation=1)
        self.dc_conv2_1 = conv(48, 48, kernel_size=3, stride=1, padding=2, dilation=2)
        self.dc_conv2_2 = conv(48, 32, kernel_size=3, stride=1, padding=4, dilation=4)
        self.predict_flow2b = predict_flow(32)

        od = 1 + 16 + 16 + 3
        self.conv1_0 = conv_block(dim, od, 48, 1)
        self.conv1_1 = conv_block(dim, 48, 32, 1)
        self.conv1_2 = conv_block(dim, 32, 16, 1)
        self.predict_flow1a = predict_flow(16)

        self.dc_conv1_0 = conv(3, 48, kernel_size=3, stride=1, padding=1, dilation=1)
        self.dc_conv1_1 = conv(48, 48, kernel_size=3, stride=1, padding=2, dilation=2)
        self.dc_conv1_2 = conv(48, 32, kernel_size=3, stride=1, padding=4, dilation=4)
        self.predict_flow1b = predict_flow(32)

        self.resize = ResizeTransform(1 / 2, dim)
        self.integrate2 = VecInt(down_shape2, int_steps)
        self.integrate1 = VecInt(down_shape1, int_steps)

    def forward(self, tgt, src):
        c11, c21, c12, c22 = self.FeatureLearning(tgt, src)

        corr2 = MatchCost(c22, c12)
        x = torch.cat((corr2, c22), 1)
        x = self.conv2_0(x)
        x = self.conv2_1(x)
        x = self.conv2_2(x)
        flow2 = self.predict_flow2a(x)
        upfeat2 = self.resize(x)

        x = self.dc_conv2_0(flow2)
        x = self.dc_conv2_1(x)
        x = self.dc_conv2_2(x)
        refine_flow2 = self.predict_flow2b(x) + flow2
        int_flow2 = self.integrate2(refine_flow2)
        up_int_flow2 = self.resize(int_flow2)
        features_s_warped = self.spatial_transform_f(c11, up_int_flow2)

        corr1 = MatchCost(c21, features_s_warped)
        x = torch.cat((corr1, c21, up_int_flow2, upfeat2), 1)
        x = self.conv1_0(x)
        x = self.conv1_1(x)
        x = self.conv1_2(x)
        flow1 = self.predict_flow1a(x) + up_int_flow2

        x = self.dc_conv1_0(flow1)
        x = self.dc_conv1_1(x)
        x = self.dc_conv1_2(x)
        refine_flow1 = self.predict_flow1b(x) + flow1
        int_flow1 = self.integrate1(refine_flow1)
        flow = self.resize(int_flow1)
        y = self.spatial_transform(src, flow)
        flow_pyramid = [int_flow1, refine_flow1, int_flow2, refine_flow2]
        return y, flow, flow_pyramid
    
class MixedOp(nn.Module):
    def __init__(self, in_channels, out_channels, stride):
        super(MixedOp, self).__init__()
        self._ops = nn.ModuleList()
        for primitive in PRIMITIVES:
            op = OPS[primitive](in_channels, out_channels, stride)
            self._ops.append(op)

    def forward(self, x, weights):
        return sum(w * op(x) for w, op in zip(weights, self._ops))
    
class Cell(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(Cell, self).__init__()
        self.op = MixedOp(in_channels, out_channels, stride)

    def forward(self, x, weights):
        out = self.op(x, weights)
        return out
    
class MatchCost_Cell(nn.Module):
    def __init__(self, PRIMITIVES):
        super(MatchCost_Cell, self).__init__()
        self.Primitives = PRIMITIVES

        self.enc_2 = nn.ModuleList()
        self.enc_1 = nn.ModuleList()

        self.enc_2.append(Cell_Op(self.Primitives, 33, 48, 1))  # 2层 (in_channels, out_channels, stride=1)
        self.enc_2.append(Cell_Op(self.Primitives, 48, 32, 1))  # 2层
        self.enc_2.append(Cell_Op(self.Primitives, 32, 16, 1))  # 2层

        self.enc_1.append(Cell_Op(self.Primitives, 36, 48, 1))  # 1层
        self.enc_1.append(Cell_Op(self.Primitives, 48, 32, 1))  # 1层
        self.enc_1.append(Cell_Op(self.Primitives, 32, 16, 1))  # 1层

    def forward(self, src, tgt, up_int_flow, upfeat, weights):
        mc = torch.norm(src - tgt, p=1, dim=1)
        mc = mc[..., np.newaxis]
        x = mc.permute(0, 4, 1, 2, 3)
        input_list = list(src.size())
        channel = int(input_list[1])
        if channel == 16:
            x = torch.cat((x, tgt, up_int_flow, upfeat), 1)
            x = self.enc_1[2](self.enc_1[1](self.enc_1[0](x, weights[0]), weights[1]), weights[2])
        elif channel == 32:
            x = torch.cat((tgt, x), 1)
            x = self.enc_2[2](self.enc_2[1](self.enc_2[0](x, weights[0]), weights[1]), weights[2])
        return x
    
class Cell_Op(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(Cell_Op, self).__init__()
        self.op = MixedOp(in_channels, out_channels, stride)

    def forward(self, x, weights):
        out = self.op(x, weights)
        return out
    
class Concat_Cell_arc(nn.Module):

    def __init__(self, PRIMITIVES):
        super(Concat_Cell_arc, self).__init__()
        self.Primitives = PRIMITIVES

        self.enc_2 = nn.ModuleList()
        self.enc_1 = nn.ModuleList()

        self.enc_2.append(Cell_Op(64, 48, 1))  # 2 (in_channels, out_channels, stride=1)
        self.enc_2.append(Cell_Op(48, 32, 1))  # 2
        self.enc_2.append(Cell_Op(32, 16, 1))  # 2

        self.enc_1.append(Cell_Op(51, 48, 1))  # 1
        self.enc_1.append(Cell_Op(48, 32, 1))  # 1
        self.enc_1.append(Cell_Op(32, 16, 1))  # 1

    def forward(self, src, tgt, up_int_flow, upfeat, weights):
        input_list = list(src.size())
        channel = int(input_list[1])
        if channel == 16:
            x = torch.cat((src, tgt, up_int_flow, upfeat), 1)
            x = self.enc_1[2](self.enc_1[1](self.enc_1[0](x, weights[0]), weights[1]), weights[2])
        elif channel == 32:
            x = torch.cat((src, tgt), 1)
            x = self.enc_2[2](self.enc_2[1](self.enc_2[0](x, weights[3]), weights[4]), weights[5])
        return x
    
class Refine_Cell(nn.Module):

    def __init__(self, PRIMITIVES):
        super(Refine_Cell, self).__init__()
        self.Primitives = PRIMITIVES

        self.enc_2 = nn.ModuleList()
        self.enc_1 = nn.ModuleList()

        self.enc_2.append(Cell_Op(self.Primitives, 65, 48, 1))  # 2层 (in_channels, out_channels, stride=1)
        self.enc_2.append(Cell_Op(self.Primitives, 48, 32, 1))  # 2层
        self.enc_2.append(Cell_Op(self.Primitives, 32, 16, 1))  # 2层

        self.enc_1.append(Cell_Op(self.Primitives, 52, 48, 1))  # 1层
        self.enc_1.append(Cell_Op(self.Primitives, 48, 32, 1))  # 1层
        self.enc_1.append(Cell_Op(self.Primitives, 32, 16, 1))  # 1层

    def forward(self, src, tgt, up_int_flow, upfeat, weights):
        mc = torch.norm(src - tgt, p=1, dim=1)
        mc = mc[..., np.newaxis]
        x = mc.permute(0, 4, 1, 2, 3)
        input_list = list(src.size())
        channel = int(input_list[1])
        if channel == 16:
            x = torch.cat((src, tgt, x, up_int_flow, upfeat), 1)
            x = self.enc_1[2](self.enc_1[1](self.enc_1[0](x, weights[0]), weights[1]), weights[2])
        elif channel == 32:
            x = torch.cat((src, tgt, x), 1)
            x = self.enc_2[2](self.enc_2[1](self.enc_2[0](x, weights[0]), weights[1]), weights[2])
        return x
    
Cell_Operation = {
    'MatchCost_Cell': lambda genotype: MatchCost_Cell(PRIMITIVES),
    'Concat_Cell_arc': lambda genotype: Concat_Cell_arc(PRIMITIVES),
    'Refine_Cell': lambda genotype: Refine_Cell(PRIMITIVES),
}

def predict_flow(in_planes):
    dim = 3
    conv_fn = getattr(nn, 'Conv%dd' % dim)
    return conv_fn(in_planes, dim, kernel_size=3, padding=1)

def conv(in_planes, out_planes, kernel_size=3, stride=1, padding=1, dilation=1):
    return nn.Sequential(
        nn.Conv3d(in_planes, out_planes, kernel_size=kernel_size, stride=stride,
                  padding=padding, dilation=dilation, bias=True),
        nn.LeakyReLU(0.1))

def MatchCost(features_t, features_s):
    mc = torch.norm(features_t - features_s, p=1, dim=1)
    mc = mc[ ..., np.newaxis]
    return mc.permute(0, 4, 1, 2, 3)
