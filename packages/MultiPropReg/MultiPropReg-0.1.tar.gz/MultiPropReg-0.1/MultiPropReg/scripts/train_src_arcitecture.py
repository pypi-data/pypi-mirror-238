"""
Example script to train a MultiPropReg model. 

You will likely have to customize this script slightly to accommodate your own data.
You can customize the paths for your training data (using your own dataset), the atlas 
standard image (if not provided, the default atlas image will be used), the output path, 
etc. Moreover, this training code is equipped to automatically search for the optimal 
network structure, which will be used in constructing the registration network. You can 
define how the network structure is to be searched by specifying training parameters.

Example usage is:

    python MultiPropReg/scripts/train_src_arcitecture.py \
        --load_model model.ckpt \
        --data /path/to/dataset \
        --atlas /path/to/atlas_file \
        --model_path /path/to/model_output_folder \
        --gpu  device_id \
        --arch_tag 0/1/2/3 \
        --epochs 100

    arch_tag 0 :Search for feature extraction.
    arch_tag 1 :Search for deformation estimation.
    arch_tag 2 :Search for the entire network.
    arch_tag 3 :Conduct training only, without searching.

More information is available at scrpits/README.md.

"""

import os
import sys
sys.path.append('../MultiPropReg')
import glob
import logging
import argparse
import torch.utils
import torch.backends.cudnn as cudnn
import random
import torch.utils.data as da
from torch.optim import Adam
from MultiPropReg.torch.architect_v5 import Architect
import MultiPropReg.datagenerators as datagenerators
from MultiPropReg.torch.losses import *
from MultiPropReg.torch.networks import *
import MultiPropReg.torch.utils as utils

parser = argparse.ArgumentParser("cifar")

# data organization parameters
parser.add_argument('--data', type=str, default='data/divided_dataset/Train_Affine', help='location of the data corpus')
parser.add_argument('--data_model', type=int, default=0)
parser.add_argument('--load_model', help='optional model file to initialize with')
parser.add_argument('--model_path', type=str, default='saved_models', help='path to save the model')
parser.add_argument('--atlas', help='atlas filename (default: data/1yr_t1_atlas.nii)')

# training parameters
parser.add_argument('--batch_size', type=int, default=1, help='batch size')
parser.add_argument('--learning_rate', type=float, default=3e-4, help='init learning rate')
parser.add_argument('--momentum', type=float, default=0.9, help='momentum')
parser.add_argument('--weight_decay', type=float, default=0, help='weight decay')
parser.add_argument('--report_freq', type=float, default=1, help='report frequency')
parser.add_argument('--gpu', type=int, default=0, help='gpu device id')
parser.add_argument('--epochs', type=int, default=45, help='num of training epochs')
parser.add_argument('--cutout', action='store_true', default=False, help='use cutout')
parser.add_argument('--cutout_length', type=int, default=16, help='cutout length')
parser.add_argument('--drop_path_prob', type=float, default=0.3, help='drop path probability')
parser.add_argument('--seed', type=int, default=2, help='random seed')
parser.add_argument('--grad_clip', type=float, default=5, help='gradient clipping')
parser.add_argument('--train_portion', type=float, default=0.5, help='portion of training data')
parser.add_argument('--unrolled', action='store_true', default=True, help='use one-step unrolled validation loss')
parser.add_argument('--arch_learning_rate', type=float, default=1e-4, help='learning rate for arch encoding')
parser.add_argument('--arch_weight_decay', type=float, default=0, help='weight decay for arch encoding')
parser.add_argument('--shape', type=list, default=[160, 192, 224], help='weight decay for arch encoding')

# searching parameters
parser.add_argument('--feature_operations', nargs='+', default=['conv_3x3']*6, 
                    help='List of operations for FeatureExtraction module')
parser.add_argument('--estimator_operations', nargs='+', default=['conv_3x3']*6, 
                    help='List of operations for Estimator module')
parser.add_argument('--search_tag', type=bool, default=False, help='weight decay for arch encoding')
parser.add_argument('--arch_tag', type=int, default=0, help='weight decay for arch encoding')

args = parser.parse_args()

# prepare model folder
model_dir = args.model_path
os.makedirs(model_dir, exist_ok=True)

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

    if args.gpu is not None:
        if args.data_model == 0:
            criterion = LossFunction_ncc().cuda()
        if args.data_model == 1:
            criterion = LossFunction_mind().cuda()
    else:
        if args.data_model == 0:
            criterion = LossFunction_ncc()
        if args.data_model == 1:
            criterion = LossFunction_mind()

    if args.arch_tag == 0:
        model = Network_Search_Feature(criterion, args.shape, operations=args.estimator_operations)
        args.search_tag = True
    if args.arch_tag == 1:  
        model = Network_Search_Estimator(criterion, 'Concat_Cell_arc', args.shape, operations=args.feature_operations)
        args.search_tag = True
    if args.arch_tag == 2:   
        model = Network_Search_all(criterion, 'Concat_Cell_arc', args.shape)
        args.search_tag = True
    if args.arch_tag == 3:
         model = Deformable(criterion, args.shape, feature_operations=args.feature_operations, estimator_operations=args.estimator_operations)
         args.search_tag = False
    
    if args.gpu is not None:
        model = model.cuda()
    # load initial model (if specified)
    if args.load_model:
        if args.gpu is not None:
            model.load_state_dict(torch.load(args.load_model))
        else:
            model.load_state_dict(torch.load(args.load_model, map_location=torch.device('cpu')))
    

    logging.info("param size = %fMB", utils.count_parameters_in_MB(model))

    optimizer = Adam(model.parameters(), lr=args.learning_rate)

    # data generator
    train_vol_names = glob.glob(os.path.join(args.data, '*.nii.gz'))
    random.shuffle(train_vol_names)
    if args.atlas:
        atlas_file = args.atlas
    else:
        atlas_file = 'MultiPropReg/data/1yr_t1_atlas.nii'
    train_data = datagenerators.MRIDataset(train_vol_names, atlas_file)
    num_train = len(train_vol_names)
    indices = list(range(num_train))
    split = int(np.floor(args.train_portion * num_train))

    train_queue = da.DataLoader(
        train_data, batch_size=args.batch_size,
        sampler=da.sampler.SubsetRandomSampler(indices[:split]),
        pin_memory=True, num_workers=1)

    valid_queue = da.DataLoader(
        train_data, batch_size=args.batch_size,
        sampler=da.sampler.SubsetRandomSampler(indices[split:num_train]),
        pin_memory=True, num_workers=1)

    if args.search_tag:
        architect = Architect(model, args)

    for epoch in range(0, args.epochs):
        lr = args.learning_rate
        if args.search_tag: 
            genotype = model.genotype()
            logging.info('genotype = %s', genotype)

        if args.arch_tag == 0 or args.arch_tag == 1:
            logging.info(F.softmax(model.alphas, dim=-1))
        if args.arch_tag == 2:
            logging.info(F.softmax(model.alphas_fea, dim=-1))
            logging.info(F.softmax(model.alphas_op, dim=-1)) 

        # training
        if args.search_tag:
            loss = train(train_queue, valid_queue, model, architect, optimizer, lr, epoch)
        else:
            loss = train(train_queue, valid_queue, model, None, optimizer, lr, epoch)
        logging.info('train_loss of %03d epoch : %f', epoch, loss.item())

        tmp = epoch
        save_file_name = os.path.join(args.model_path, '%d.ckpt' % tmp)
        torch.save(model.state_dict(), save_file_name)


def train(train_queue, valid_queue, model, architect, optimizer, lr, epoch):
    loss_all = []
    for step, (input, target) in enumerate(train_queue):
        model.train()

        if args.gpu is not None:
            input = Variable(input, requires_grad=False).cuda()
            target = Variable(target, requires_grad=False).cuda(non_blocking=True)
        else:
            input = Variable(input, requires_grad=False)
            target = Variable(target, requires_grad=False)

        if epoch >= 15 and args.search_tag:
            input_search, target_search = next(iter(valid_queue))
            if args.gpu is not None:
                input_search = Variable(input_search, requires_grad=False).cuda()
                target_search = Variable(target_search, requires_grad=False).cuda(non_blocking=True)
            else:
                input_search = Variable(input_search, requires_grad=False)
                target_search = Variable(target_search, requires_grad=False)
            architect.step(input, target, input_search, target_search, lr, optimizer, unrolled=args.unrolled)

        optimizer.zero_grad()
        loss, sim, grad = model._loss(input, target)

        loss.backward()
        nn.utils.clip_grad_norm(model.parameters(), args.grad_clip)
        optimizer.step()

        if step % args.report_freq == 0:
            logging.info('train %03d  %f,  %f, %f', step, loss, sim, grad)
        loss_all.append(loss.item())
    
    return np.average(loss_all)


if __name__ == '__main__':
    main()
