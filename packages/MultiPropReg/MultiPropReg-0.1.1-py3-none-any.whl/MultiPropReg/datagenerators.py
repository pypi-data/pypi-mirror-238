import numpy as np
import sys
import random
import torch
from torchvision import transforms
from torch.utils.data import Dataset
import nibabel as nib
from MultiPropReg.convert_lablels import convert
from scipy import ndimage


def load_example_by_name(vol_name, seg_name=None):
    """
    load a specific volume and segmentation
    """
    X = nib.load(vol_name).get_fdata()

    # normalize
    X = normalize(X)
    # X = n_score_normalize(X)
    
    X = np.reshape(X, (1,) + X.shape + (1,))

    return_vals = [X]

    if(seg_name):
        X_seg = nib.load(seg_name).get_fdata()
        X_seg = np.reshape(X_seg, (1,) + X_seg.shape + (1,))
        return_vals.append(X_seg)
        return_vals.append(nib.load(vol_name))

    return tuple(return_vals)


def load_volfile(datafile):
    """
    load volume file
    formats: nii, nii.gz, mgz, npz
    if it's a npz (compressed numpy), assume variable names 'vol_data'
    """
    assert datafile.endswith(('.nii', '.nii.gz', '.mgz', '.npz')), 'Unknown data file: %s' % datafile

    if datafile.endswith(('.nii', '.nii.gz', '.mgz')):
        # import nibabel
        if 'nib' not in sys.modules:
            try:
                import nibabel as nib
            except:
                print('Failed to import nibabel. need nibabel library for these data file types.')

        X = nib.load(datafile).get_fdata()

    else:  # npz
        X = np.load(datafile)['vol_data']

    return X


def normalize(data):
    max = data.max()
    min = data.min()
    return (data - min) / (max - min)


def n_score_normalize(data):
    """Normalize as n-score and minus minimum
    """
    mean = data.mean()
    std = np.std(data)
    data = (data - mean) / std
    return data - data.min()


class MRIDataset(Dataset):
    def __init__(self, train_vol_names, atlas_file):
        self.train_vol_names = train_vol_names
        self.len = len(self.train_vol_names)
        self.atlas_file = atlas_file

        '''class torchvision.transforms.ToTensor'''
        self.toTensor = transforms.ToTensor()

    def __getitem__(self, i):
        index = i % self.len
        X = load_volfile(self.train_vol_names[index])
        
        # atlas_idx = random.randint(0,self.len) % self.len
        # atlas = load_volfile(self.train_vol_names[atlas_idx])
        atlas = load_volfile(self.atlas_file)

        # Set data shape
        X = ndimage.zoom(X, (160 / X.shape[0], 192 / X.shape[1], 224 / X.shape[2]), order=1)
        atlas = ndimage.zoom(atlas, (160 / atlas.shape[0], 192 / atlas.shape[1], 224 / atlas.shape[2]), order=1)

        atlas = normalize(atlas)
        # atlas = n_score_normalize(atlas)
        atlas = self.toTensor(atlas)
        atlas = atlas[np.newaxis, ...]
        atlas = atlas.permute(0, 2, 3, 1).float()
        X = normalize(X)
        # X = n_score_normalize(X)
        X = self.toTensor(X)
        X = X[np.newaxis, ...]
        X = X.permute(0, 2, 3, 1).float()
        # print(f'min: {X.min()}   max: {X.max()}')

        return X, atlas

    def __len__(self):
        return len(self.train_vol_names)
    
class MRIDatasetWithMask(Dataset):
    def __init__(self, train_vol_names, atlas_dir, atlas_seg_dir):
        self.train_vol_names = train_vol_names
        self.atlas_dir = atlas_dir
        self.atlas_seg_dir = atlas_seg_dir
        '''class torchvision.transforms.ToTensor'''
        self.toTensor = transforms.ToTensor()

    def __getitem__(self, i):
        Source_image  = self.train_vol_names[i]
        seg_path_1 = Source_image.replace('vol', 'seg')

        Target_image = self.atlas_dir
        seg_path_0 = self.atlas_seg_dir

        image_0 = load_volfile(Target_image)
        image_0 = torch.Tensor(image_0).float()
        image_0 = image_0.unsqueeze(0)

        image_1 = load_volfile(Source_image)
        image_1 = torch.Tensor(image_1).float()
        image_1 = image_1.unsqueeze(0)

        mask_0 = load_volfile(seg_path_0)
        mask_1 = load_volfile(seg_path_1)
        mask_0, mask_1 = convert(mask_0), convert(mask_1)

        mask_0 = torch.Tensor(mask_0).float()
        mask_1 = torch.Tensor(mask_1).float()
        mask_0 = mask_0.unsqueeze(0)
        mask_1 = mask_1.unsqueeze(0)

        return image_0, image_1, mask_0, mask_1

    def __len__(self):
        return len(self.train_vol_names)


class T1T2Dataset(Dataset):
    def __init__(self, train_vol_names, atlas_file):
        self.train_vol_names = train_vol_names
        self.len = len(self.train_vol_names)
        self.atlas_file = atlas_file

        '''class torchvision.transforms.ToTensor'''
        self.toTensor = transforms.ToTensor()

    def __getitem__(self, i):
        atlas = load_volfile(self.atlas_file)
        atlas = self.toTensor(atlas)
        atlas = atlas[np.newaxis, ...]
        atlas = atlas.permute(0, 2, 3, 1).float()
        index = i % self.len
        X = load_volfile(self.train_vol_names[index])
        X = self.toTensor(X)
        X = X[np.newaxis, ...]
        X = X.permute(0, 2, 3, 1).float()

        return X, atlas

    def __len__(self):
        return len(self.train_vol_names)