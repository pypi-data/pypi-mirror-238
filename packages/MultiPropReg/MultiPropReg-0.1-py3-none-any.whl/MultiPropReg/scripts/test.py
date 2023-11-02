"""
Example script for testing quality of trained MultiPropReg models. This script iterates over a list of
images pairs, registers them, propagates segmentations via the deformation, and computes the dice
overlap. Example usage is:

    python MultiPropReg/scripts/test.py  \
        --model model.ckpt  \
        --atlas /path/to/atlas_file  \
        --atlas_seg  /path/to/atlas_seg_file
        --image_path  /path/to/dataset  \
        --result_save  /path/to/img_output_folder  \
        --gpu  device_id  \
        --hyper_parameters 10,15,3.2,0.8
 
You can customize the parameters of this script and use your own dataset for testing.
"""

import os, glob
import sys
sys.path.append('../MultiPropReg')
import argparse
from MultiPropReg.datagenerators import *
from MultiPropReg.torch.losses import *
from MultiPropReg.torch.networks import *
from MultiPropReg.torch.layers import *
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
import scipy.io as sio
from scipy import ndimage

# parse the commandline
parser = argparse.ArgumentParser("T1-to-T1atlas")

# set parameters
parser.add_argument('--model', type=str, default='load_models', help='path to load the model')
parser.add_argument('--atlas', help='atlas filename (default: data/1yr_t1_atlas.nii)')
parser.add_argument('--atlas_seg', help='atlas filename (default: data/1yr_t1_atlas_seg.nii)')
parser.add_argument('--image_path', required=True, help='list of testing files')
parser.add_argument('--result_save', type=str, default='HO-MPR', help='experiment name')
parser.add_argument('--gpu', type=int, default=0, help='GPU number(s) - if not supplied, CPU is used') 
parser.add_argument('--feature_operations', nargs='+', default=['conv_3x3']*6, 
                    help='List of operations for FeatureExtraction module')
parser.add_argument('--estimator_operations', nargs='+', default=['conv_3x3']*6, 
                    help='List of operations for Estimator module')
parser.add_argument('--hyper_parameters', type=str, default=None, 
                    help='List of hyperparameters (e.g., "10,15,3.2,0.8")')


args = parser.parse_args()

"""  *********************** Segmentation Related *************************** """

def dice(vol1, vol2, labels=None, nargout=1):
    '''
    Dice [1] volume overlap metric

    The default is to *not* return a measure for the background layer (label = 0)

    [1] Dice, Lee R. "Measures of the amount of ecologic association between species."
    Ecology 26.3 (1945): 297-302.

    Parameters
    ----------
    vol1 : nd array. The first volume (e.g. predicted volume)
    vol2 : nd array. The second volume (e.g. "true" volume)
    labels : optional vector of labels on which to compute Dice.
        If this is not provided, Dice is computed on all non-background (non-0) labels
    nargout : optional control of output arguments. if 1, output Dice measure(s).
        if 2, output tuple of (Dice, labels)

    Output
    ------
    if nargout == 1 : dice : vector of dice measures for each labels
    if nargout == 2 : (dice, labels) : where labels is a vector of the labels on which
        dice was computed
    '''
    if labels is None:
        labels = np.unique(np.concatenate((vol1, vol2)))
        labels = np.delete(labels, np.where(labels == 0))  # remove background

    dicem = np.zeros(len(labels))
    for idx, lab in enumerate(labels):
        vol1l = vol1 == lab
        vol2l = vol2 == lab
        top = 2 * np.sum(np.logical_and(vol1l, vol2l))
        bottom = np.sum(vol1l) + np.sum(vol2l)
        bottom = np.maximum(bottom, np.finfo(float).eps)  # add epsilon.
        dicem[idx] = top / bottom

    if nargout == 1:
        return dicem
    else:
        return (dicem, labels)
    
def parse_hyper_parameters(value):
    if value is None:
        return [10, 15, 3.2, 0.8]
    return [float(val) for val in value.split(',')]

# device handling
if args.gpu is not None:
    device = 'cuda'
    os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu)
else:
    device = 'cpu'
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    
def test(model_file, dataset_dir, result_save):

    # Set the shape of images
    shape = [160, 192, 224]

    # Load and set up model
    if args.gpu is not None:
        criterion = LossFunction_Registration().cuda()
        if args.hyper_parameters:
            model = MPR_net_Hyper1(criterion, args.feature_operations, args.estimator_operations).cuda()
        else:
            model = MPR_net_noHyper1(criterion, args.feature_operations, args.estimator_operations).cuda()

    else:
        criterion = LossFunction_Registration()
        if args.hyper_parameters:
            model = MPR_net_Hyper1(criterion, args.feature_operations, args.estimator_operations)
        else:
            model = MPR_net_noHyper1(criterion, args.feature_operations, args.estimator_operations)

    model.eval()

    model.load_state_dict(torch.load(model_file, map_location='cpu'), strict=False)

    # Use this to warp segments
    trf = SpatialTransformer(shape, mode='nearest')
    if args.gpu is not None:
        trf = trf.cuda()

    trf1 = SpatialTransformer(shape)
    if args.gpu is not None:
        trf1 = trf1.cuda()

    ncc_list0, ncc_list1, dice_list0, dice_list1 = [], [], [], []
    jdv_list = []
    jdv_list1 = []

    os.makedirs(result_save, exist_ok=True)

    image_path_table = glob.glob(dataset_dir+'/*')

    print(f'Using model: {model_file}')

    for image_path in image_path_table:
        # Load Image

        Source_image = image_path
        if args.atlas is None or args.atlas == '':
            args.atlas = 'data/1yr_t1_atlas.nii'
        Target_image = args.atlas
        Target_seg = args.atlas_seg

        image_0, image_1 = load_volfile(Target_image), load_volfile(Source_image)

        # Resize and normalize the image
        image_0 = ndimage.zoom(image_0, (160 / 180, 192 / 220, 224 / 180), order=1)
        image_1 = ndimage.zoom(image_1, (160 / 180, 192 / 220, 224 / 180), order=1)

        image_0 = normalize(image_0)
        image_1 = normalize(image_1)

        if args.gpu is not None:
            image_0 = torch.Tensor(image_0).cuda().float()
            input_fixed = image_0.unsqueeze(0).unsqueeze(0)
            image_1 = torch.Tensor(image_1).cuda().float()
            input_moving = image_1.unsqueeze(0).unsqueeze(0)
        else:
            image_0 = torch.Tensor(image_0).float()
            input_fixed = image_0.unsqueeze(0).unsqueeze(0)
            image_1 = torch.Tensor(image_1).float()
            input_moving = image_1.unsqueeze(0).unsqueeze(0)

        if Target_seg:
            mask_1 = load_volfile(Target_seg)
            mask_1 = ndimage.zoom(mask_1, (160 / 180, 192 / 220, 224 / 180), order=0)
            if args.gpu is not None:
                mask_1 = torch.Tensor(mask_1).cuda().float()
            else:
                mask_1 = torch.Tensor(mask_1).float()
            mask_1 = mask_1.unsqueeze(0).unsqueeze(0)

        # Run Model
        with torch.no_grad():
            warped_src, flow, int_flow1, int_flow2,_, _ = model(input_moving, input_fixed)

        # Warp segment using flow
        if args.atlas_seg is not None:
                warp_seg = trf(mask_1, flow).cpu().numpy().squeeze()
                new_image = warped_src.cpu().numpy().squeeze()
                new_image = nib.Nifti1Image(new_image, np.eye(4))

        oname = Source_image.split(os.sep)[-1]
        nib.save(nib.Nifti1Image(warped_src.cpu().numpy().squeeze(), np.eye(4)), os.path.join(result_save, oname))
        if args.atlas_seg is not None:
                nib.save(nib.Nifti1Image(warp_seg, np.eye(4)), os.path.join(result_save, oname.replace('.nii.gz', '_seg.nii.gz')))

        print(f"'{os.path.basename(Source_image)}' : wrapped image generated")
        
        if args.atlas_seg is not None:

                print('mean:' + str(np.mean(dice_list0)))
                print('std:' + str(np.std(dice_list0)))
                dice.write('before mean:' + str(np.mean(dice_list0)) + '\n')
                dice.write('before std:' + str(np.std(dice_list0)) + '\n') 

                print('mean:' + str(np.mean(dice_list1)))
                print('std:' + str(np.std(dice_list1)))
                dice.write('After_Dice_mean:' + str(np.mean(dice_list1)) + '\n')
                dice.write('After_Dice_std:' + str(np.std(dice_list1)) + '\n')

if __name__ == "__main__":

    if args.model is None or args.model == '':
        args.model = 'models/pretrained_model_epoch400.ckpt'
    if args.image_path is None or args.image_path == '':
        args.image_path = 'data/divided_dataset/Test_Affine'
    if args.result_save is None or args.result_save == '':
        args.result_save = 'output'
    if args.hyper_parameters is not None:
        args.hyper_parameters = parse_hyper_parameters(args.hyper_parameters)

    test(args.model, args.image_path, args.result_save)
