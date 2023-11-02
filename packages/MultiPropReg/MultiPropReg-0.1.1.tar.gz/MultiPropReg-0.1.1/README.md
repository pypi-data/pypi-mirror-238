# MultiPropReg: Learning Deformable Image Registration from Optimization: Perspective, Modules, Bilevel Training and Beyond

**MultiPropReg** is a general purpose library for learning-based tools for alignment/registration, and more generally modelling with deformations.




## Pre-trained models

See list of pre-trained models available [here](models/pretrained_model_epoch400.ckpt).

## Training

If you would like to train your own model, you will likely need to customize some of the data-loading code in `MultiPropReg/datagenerators.py` for your own datasets and data formats. Training data can be in the NII, MGZ, or npz (numpy) format, and it's assumed that each npz file in your data list has a `vol` parameter, which points to the image data to be registered, and an optional `seg` variable, which points to a corresponding discrete segmentation (for semi-supervised learning). The training data we provide has been skull removed and affine registered, if you need to process your own data, you can use the tools we provide to do the data processing.

We have defined three training modes:  
`train_src_arcitecture.py`: architecture-search training;  
`train_src_hyper.py`: hyper parameter-search training (without segmentation data);  
`train_src_hyper_seg.py`: hyper parameter-search training (with segmentation data);

Detailed usage instructions can be found in scripts/README.md.


## Testing

If you want to test the training results, you can use our example:

```
python MultiPropReg/scripts/test.py  \
        --model MultiPropReg/models/pretrained_model_epoch400.ckpt \
        --atlas MultiPropReg/data/1yr_t1_atlas.nii  \
        --atlas_seg  /path/to/atlas_seg_file  \
        --image_path MultiPropReg/data/divided_dataset/Test_Affine  \
        --result_save MultiPropReg/output_test_400  \
        --gpu 0
        --hyper_parameters
```

If you have a dataset with segmented images, you have the option to manually specify the `atlas_seg` parameter. Additionally, we offer a selection of pre-trained models for a rapid assessment of registration outcomes.
Detailed usage instructions can be found in scripts/README.md.


