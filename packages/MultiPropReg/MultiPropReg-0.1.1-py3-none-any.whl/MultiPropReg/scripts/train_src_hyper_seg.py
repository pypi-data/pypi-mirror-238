"""
Example script to train a MultiPropReg model. 

You will likely have to customize this script slightly to accommodate your own data.
You can customize the paths for your training data (using your own dataset), the atlas 
standard image (if not provided, the default atlas image will be used), the output path, 
etc. The training code can automatically search for optimal hyperparameters when segmentation 
maps are provided. This functionality can be applied in subsequent training and testing processes.
You can define how the network structure is to be searched by specifying training parameters.

Example usage is:

    python MultiPropReg/scripts/train_src_hyper_seg.py  \
        --load_model model.ckpt  \
        --data_dir /path/to/dataset  \
        --atlas /path/to/atlas_file  \
        --atlas_seg /path/to/atlas_seg_file  \
        --model_path  /path/to/model_output_folder  \
        --gpu  device_id  \
        --epochs 50 \
        --search_hyper

More information is available at scrpits/README.md.
"""

import os
import sys

sys.path.append('../MultiPropReg')
import numpy as np
import glob
import logging
import argparse
import torch.utils
import torch.backends.cudnn as cudnn
from torch.autograd import Variable
from MultiPropReg.hyper_optimizer import HyperOptimizer
from MultiPropReg.upperoptimizer import HyperGradient
import MultiPropReg.datagenerators as datagenerators
import random
import torch.utils.data as da
from torch.optim import Adam
from MultiPropReg.torch.losses import *
from MultiPropReg.torch.networks import *

from torch.utils.tensorboard import SummaryWriter

# parse the commandline
parser = argparse.ArgumentParser("T1-to-T1atlas")

# data organization parameters
parser.add_argument('--data_dir', help='list of training files', default='data1/wangxiaolin/Unet-RegSeg/Data/Test_data/vol')
parser.add_argument('--atlas', help='atlas filename (default: data/atlas_vol.nii)')
parser.add_argument('--atlas_seg', help='atlas segmentation filename (default: data/atlas_seg_14labels.nii)')
parser.add_argument('--model_path', type=str, default='saved_models', help='path to save the model')

# training parameters
parser.add_argument('--gpu', type=int, default=0, help='gpu device id') 
parser.add_argument('--batch_size', type=int, default=1, help='batch size')
parser.add_argument('--epochs', type=int, default=500, help='num of training epochs') 
parser.add_argument('--load_model', help='optional model file to initialize with')
parser.add_argument('--initial-epoch', type=int, default=0, help='initial epoch number (default: 0)')
parser.add_argument('--learning_rate', type=float, default=1e-4, help='init learning rate')
parser.add_argument('--momentum', type=float, default=0.9, help='momentum')
parser.add_argument('--report_freq', type=float, default=1, help='report frequency')
parser.add_argument('--seed', type=int, default=2, help='random seed')
parser.add_argument('--grad_clip', type=float, default=5, help='gradient clipping')
parser.add_argument('--train_portion', type=float, default=0.5, help='portion of training data')
parser.add_argument('--unrolled', action='store_true', default=True, help='use one-step unrolled validation loss')
parser.add_argument('--arch_learning_rate', type=float, default=1e-4, help='learning rate for arch encoding')
parser.add_argument('--weight_decay', type=float, default=0, help='weight decay value')
parser.add_argument('--arch_weight_decay', type=float, default=0, help='architecture weight decay value')
parser.add_argument('--multi_modal', action='store_true', default=False, help='Whether the data is multi-modal')

# searching parameters
parser.add_argument('--feature_operations', nargs='+', default=['conv_3x3']*6, 
                    help='List of operations for FeatureExtraction module')
parser.add_argument('--estimator_operations', nargs='+', default=['conv_3x3']*6, 
                    help='List of operations for Estimator module')
parser.add_argument('--search_hyper', action='store_true', default=False, help='whether to use hyperparameter search')
parser.add_argument('--hyper_parameters', type=int, default=[10, 15, 3.2, 0.8, 0.5], help='initial hyperparameters')


args = parser.parse_args()

# prepare model folder
model_dir = args.model_path
os.makedirs(model_dir, exist_ok=True)

# Log configuration
log_format = '%(asctime)s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, 
    format=log_format, datefmt='%m/%d %I:%M:%S %p')
fh = logging.FileHandler(os.path.join(args.model_path, 'log.txt'))
fh.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(fh)

writer = SummaryWriter(log_dir=args.model_path, flush_secs=30)

def main():
    # device handling
    device = 'cpu'
    if args.gpu is not None:
        device = 'cuda'
        os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu)
        np.random.seed(args.seed)
        torch.cuda.set_device(args.gpu)
        cudnn.benchmark = True
        torch.manual_seed(args.seed)
        cudnn.enabled=True
        torch.cuda.manual_seed(args.seed)
        logging.info('gpu device = %d' % args.gpu)
        logging.info("args = %s", args)
    else:
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

    # configure new model
    if args.gpu is not None:
        if args.search_hyper:
            criterion_reg = LossFunction_NCCMIND().cuda()
            criterion_seg = LossFunction_dice().cuda()
        else:
            if args.multi_modal:
                criterion_reg = LossFunction_ncc().cuda()
            else:
                criterion_reg = LossFunction_mind().cuda()
    else:
        if args.search_hyper:
            criterion_reg = LossFunction_NCCMIND()
            criterion_seg = LossFunction_dice()
        else:
            if args.multi_modal:
                criterion_reg = LossFunction_ncc()
            else:
                criterion_reg = LossFunction_mind()
    
    if args.search_hyper:
        model = MPRNet_ST(criterion_reg, criterion_seg, feature_operations=args.feature_operations, estimator_operations=args.estimator_operations)
    else:
        model = Deformable(criterion_reg, shape, feature_operations=args.feature_operations, estimator_operations=args.estimator_operations)

    if args.gpu is not None:
        model = model.cuda()
    
    # load initial model (if specified)
    if args.load_model:
        if args.gpu is not None:
            model.load_state_dict(torch.load(args.load_model))
        else:
            model.load_state_dict(torch.load(args.load_model, map_location=torch.device('cpu')))

    # set optimizer
    optimizer = Adam(model.parameters(), lr=args.learning_rate)

    # data generator
    if args.data_dir is None or args.data_dir == '':
        args.data_dir = '/root/data1/wangxiaolin/Unet-RegSeg/Data/Test_data/vol'
    train_vol_names = glob.glob(os.path.join(args.data_dir, '*.nii.gz'))
    random.shuffle(train_vol_names)
    if args.atlas is None or args.atlas == '':
        args.atlas = 'MultiPropReg/data/atlas_vol.nii'
    if args.atlas_seg is None or args.atlas_seg == '':
        args.atlas_seg = 'MultiPropReg/data/atlas_seg_14labels.nii'
    atlas_file = args.atlas
    atlas_seg_file = args.atlas_seg

    if args.search_hyper:
        train_data = datagenerators.MRIDatasetWithMask(train_vol_names, atlas_file, atlas_seg_file)
    else:
        train_data = datagenerators.MRIDataset(train_vol_names, atlas_file)

    num_train = len(train_vol_names)
    indices = list(range(num_train))

    if args.search_hyper:
        train_portion = 0.5
    else:
        train_portion = 1

    split = int(np.floor(train_portion * num_train))
    print('dataset length : ', split)

    train_queue = da.DataLoader(
        train_data, batch_size=args.batch_size,
        sampler=da.sampler.SubsetRandomSampler(indices[:split]),
        pin_memory=True, num_workers=1)

    valid_queue = da.DataLoader(
        train_data, batch_size=args.batch_size,
        sampler=da.sampler.SubsetRandomSampler(indices[split:num_train]),
        pin_memory=True, num_workers=1)
    
    # Whether to use hyperparameter search
    if args.search_hyper:
        hyper_optimizer = HyperGradient(model, args)
    else:
        hyper_optimizer = None

    for epoch in range(0, args.epochs):
        lr = args.learning_rate

        # training
        loss = train(train_queue, valid_queue, model, hyper_optimizer, optimizer, lr, epoch, num_train)
        if args.search_hyper:
            logging.info('train_loss of %03d epoch : %f', epoch, loss.item())
            hyper_1 = model.hyper_1
            logging.info('hyper1 of %03d epoch : %f', epoch, hyper_1.item())
            hyper_2 = model.hyper_2
            logging.info('hyper2 of %03d epoch : %f', epoch, hyper_2.item())
            hyper_3 = model.hyper_3
            logging.info('hyper3 of %03d epoch : %f', epoch, hyper_3.item())
            hyper_4 = model.hyper_4
            logging.info('hyper4 of %03d epoch : %f', epoch, hyper_4.item())
            hyper_5 = model.hyper_5
            logging.info('hyper5 of %03d epoch : %f', epoch, hyper_5.item())

        writer.add_scalar('loss', loss.item(), epoch)

        # save model checkpoint
        if epoch % 20 == 0:
            save_file_name = os.path.join(args.model_path, '%d.ckpt' % epoch)
            torch.save(model.state_dict(), save_file_name)


def train(train_queue, valid_queue, model, hyper_optimizer, optimizer, lr, epoch, num_train):
    if args.search_hyper:
        for step, (target, source, _, _) in enumerate(train_queue):
            model.train()

            if args.gpu is not None:
                target = Variable(target, requires_grad=False).cuda()
                source = Variable(source, requires_grad=False).cuda()
            else:
                target = Variable(target, requires_grad=False)
                source = Variable(source, requires_grad=False)

            # get a random minibatch from the search queue with replacement
            if args.search_hyper:
                target_search, source_search, target_mask_search, source_mask_search = next(iter(valid_queue))
                if args.gpu is not None:
                    target_search = Variable(target_search, requires_grad=False).cuda()
                    source_search = Variable(source_search, requires_grad=False).cuda()
                    target_mask_search = Variable(target_mask_search, requires_grad=False).cuda()
                    source_mask_search = Variable(source_mask_search, requires_grad=False).cuda()
                else:
                    target_search = Variable(target_search, requires_grad=False)
                    source_search = Variable(source_search, requires_grad=False)
                    target_mask_search = Variable(target_mask_search, requires_grad=False)
                    source_mask_search = Variable(source_mask_search, requires_grad=False)

                    if epoch>=15:
                        hyper_optimizer.step(target, source, target_search, source_search, target_mask_search, source_mask_search,
                                        lr, optimizer, unrolled=args.unrolled)

            optimizer.zero_grad()
            
            if args.search_hyper:
                loss, sim, grad = model._lower_loss(target, source)
                upper_loss = model._upper_loss(target_search, source_search, target_mask_search, source_mask_search)
            else:
                loss, sim, grad = model._loss(target, source)

            loss.backward()
            nn.utils.clip_grad_norm(model.parameters(), args.grad_clip)
            optimizer.step()

            if args.search_hyper:
                if step % args.report_freq == 0:
                    logging.info('train %03d epoch %03d step loss: %f, sim: %f, grad: %f,  upper_loss: %f', 
                                    epoch, step, loss, sim, grad, upper_loss)
                    
                if step % args.report_freq == 0:
                    i = (epoch + 1) * num_train + step
                    writer.add_scalar('loss', loss, i)
                    writer.add_scalar('sim_loss', sim, i)
                    writer.add_scalar('det_loss', grad, i)
                    writer.add_scalar('upper_loss', upper_loss, i)
            else:
                if step % args.report_freq == 0:
                    logging.info('train %03d %f, %f, %f', step, loss, sim, grad)
                if step % args.report_freq == 0:
                    i = (epoch + 1) * num_train + step
                    writer.add_scalar('loss', loss, i)
    else:
        for step, (target, source) in enumerate(train_queue):
            model.train()

            if args.gpu is not None:
                target = Variable(target, requires_grad=False).cuda()
                source = Variable(source, requires_grad=False).cuda()
            else:
                target = Variable(target, requires_grad=False)
                source = Variable(source, requires_grad=False)

            # get a random minibatch from the search queue with replacement
            if args.search_hyper:
                target_search, source_search, target_mask_search, source_mask_search = next(iter(valid_queue))
                if args.gpu is not None:
                    target_search = Variable(target_search, requires_grad=False).cuda()
                    source_search = Variable(source_search, requires_grad=False).cuda()
                    target_mask_search = Variable(target_mask_search, requires_grad=False).cuda()
                    source_mask_search = Variable(source_mask_search, requires_grad=False).cuda()
                else:
                    target_search = Variable(target_search, requires_grad=False)
                    source_search = Variable(source_search, requires_grad=False)
                    target_mask_search = Variable(target_mask_search, requires_grad=False)
                    source_mask_search = Variable(source_mask_search, requires_grad=False)

                    if epoch>=15:
                        hyper_optimizer.step(target, source, target_search, source_search, target_mask_search, source_mask_search,
                                        lr, optimizer, unrolled=args.unrolled)

            optimizer.zero_grad()
            
            if args.search_hyper:
                loss, sim, grad = model._lower_loss(target, source)
                upper_loss = model._upper_loss(target_search, source_search, target_mask_search, source_mask_search)
            else:
                loss, sim, grad = model._loss(target, source)

            loss.backward()
            nn.utils.clip_grad_norm(model.parameters(), args.grad_clip)
            optimizer.step()

            if args.search_hyper:
                if step % args.report_freq == 0:
                    logging.info('train %03d epoch %03d step loss: %f, sim: %f, grad: %f,  upper_loss: %f', 
                                    epoch, step, loss, sim, grad, upper_loss)
                    
                if step % args.report_freq == 0:
                    i = (epoch + 1) * num_train + step
                    writer.add_scalar('loss', loss, i)
                    writer.add_scalar('sim_loss', sim, i)
                    writer.add_scalar('det_loss', grad, i)
                    writer.add_scalar('upper_loss', upper_loss, i)
            else:
                if step % args.report_freq == 0:
                    logging.info('train %03d %f, %f, %f', step, loss, sim, grad)
                if step % args.report_freq == 0:
                    i = (epoch + 1) * num_train + step
                    writer.add_scalar('loss', loss, i)

    return

if __name__ == '__main__':
  main() 