"""
Example script to train a MultiPropReg model. 

You will likely have to customize this script slightly to accommodate your own data.
You can customize the paths for your training data (using your own dataset), the atlas 
standard image (if not provided, the default atlas image will be used), the output path, 
etc. The training code can automatically search the optimal hyperparameters without 
providing the segmentation graph, which can be applied to the subsequent training and testing.
You can define how the network structure is to be searched by specifying training parameters.

Example usage is:

    python train_src_hyper.py  \
        --load_model model.ckpt  \
        --data_dir  /path/to/dataset  \
        --atlas /path/to/atlas_file  \
        --model_path  /path/to/model_output_folder  \
        --epochs  100 \
        --gpu  device_id  \
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
parser.add_argument('--data_dir', required=True, help='list of training files')
parser.add_argument('--atlas', help='atlas filename (default: data/1yr_t1_atlas.nii)')
parser.add_argument('--model_path', type=str, default='saved_models', help='path to save the model')

# training parameters
parser.add_argument('--gpu', type=int, default=None, help='gpu device id') 
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

# searching parameters
parser.add_argument('--feature_operations', nargs='+', default=['conv_3x3']*6, 
                    help='List of operations for FeatureExtraction module')
parser.add_argument('--estimator_operations', nargs='+', default=['conv_3x3']*6, 
                    help='List of operations for Estimator module')
parser.add_argument('--search_hyper', action='store_true', default=False, help='whether to use hyperparameter search')
parser.add_argument('--hyper_parameters', type=int, default=[10, 15, 3.2, 0.8], help='default hyperparameters')

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
        criterion = LossFunction_Registration().cuda()
    else:
        criterion = LossFunction_Registration()
    
    if args.search_hyper:
        model = MPR_net_Hyper1(criterion, feature_operations=args.feature_operations, estimator_operations=args.estimator_operations)
    else:
        model = Deformable(criterion, shape, feature_operations=args.feature_operations, estimator_operations=args.estimator_operations)

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
        args.data_dir = 'data/divided_dataset/Train_Affine'
    train_vol_names = glob.glob(os.path.join(args.data_dir, '*.nii.gz'))
    random.shuffle(train_vol_names)
    if args.atlas is None or args.atlas == '':
        args.atlas = 'data/1yr_t1_atlas.nii'
    atlas_file = args.atlas
    train_data = datagenerators.MRIDataset(
    train_vol_names, atlas_file)

    num_train = len(train_vol_names)
    indices = list(range(num_train))
    train_portion = 0.95
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
        hyper_optimizer = HyperOptimizer(model, args)
    else:
        hyper_optimizer = None

    writer = SummaryWriter('logs')
    for epoch in range(args.epochs):
        lr = args.learning_rate

        # training
        loss = train(train_queue, valid_queue, model, hyper_optimizer, criterion, optimizer, lr)
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
        
        writer.add_scalar('loss', loss.item(), epoch)


        # save model checkpoint
        if epoch % 20 == 0:
            save_file_name = os.path.join(args.model_path, '%d.ckpt' % epoch)
            torch.save(model.state_dict(), save_file_name)


def train(train_queue, valid_queue, model, hyper_optimizer, criterion, optimizer, lr):
    loss_all = []
        
    for step, (input, target) in enumerate(train_queue): # atlas, X
        model.train()

        if args.gpu is not None:
            input = Variable(input, requires_grad=False).cuda()
            target = Variable(target, requires_grad=False).cuda(non_blocking=True)
        else:
            input = Variable(input, requires_grad=False)
            target = Variable(target, requires_grad=False)

        # get a random minibatch from the search queue with replacement
        if args.search_hyper:
            input_search, target_search = next(iter(valid_queue))
            if args.gpu is not None:
                input_search = Variable(input_search, requires_grad=False).cuda()
                target_search = Variable(target_search, requires_grad=False).cuda(non_blocking=True)
            else:
                input_search = Variable(input_search, requires_grad=False)
                target_search = Variable(target_search, requires_grad=False)

            hyper_optimizer.step(input, target, input_search, target_search, lr, optimizer, unrolled=args.unrolled)

        optimizer.zero_grad()
        loss, ncc, multi, grad = model._loss(input, target)
        # loss, ncc, _ = model._loss(input, target)


        loss.backward()
        nn.utils.clip_grad_norm(model.parameters(), args.grad_clip)
        optimizer.step()

        if step % args.report_freq == 0:
            logging.info('train %03d  %f, %f, %f, %f', step, loss, ncc, multi, grad)

        loss_all.append(loss.item())

    return np.average(loss_all)

if __name__ == '__main__':
  main() 