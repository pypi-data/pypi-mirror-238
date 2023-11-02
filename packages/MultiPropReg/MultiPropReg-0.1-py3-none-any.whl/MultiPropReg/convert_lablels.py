import numpy as np
import nibabel as nib
import scipy.io as sio

labels = [0, 1, 11, 22, 33, 44, 46, 47, 48, 49, 50, 51, 52, 55]

good_labels = [0, 1, 11, 22, 33, 44, 46, 47, 48, 49, 50, 51, 52, 55]
index = list(range(len(good_labels)))

def convert(seg):
    labels = (np.unique(seg))
    extra_labels = list(set(labels).difference(set(good_labels)))

    output = np.copy(seg)
    for i in extra_labels:
        output[seg == i] = 15
    for k, v in zip(good_labels, index):
        output[seg == k ] = v
    return output