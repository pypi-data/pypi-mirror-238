# This instruction document provides some parameters for searching during training.


# Search feature extraction

`--arch_tag 0`

  when arch_tag is set to 0, it indicates that we are performing a search for feature extraction. The Network_Search_Feature model is initialized with the provided criterion and shape arguments. If you 
  have already searched the deformation estimation module , you can customize the network structure 
  by modifying the `args.estimator_operations` parameter. Conversely, if you haven't searched the 
  deformation estimation module before, you can use the default conv3 deformation estimation we provide.


# Search deformation estimation

`--arch_tag 1`

  when arch_tag is set to 1, it indicates that we are performing a search for deformation estimation. 
  The Network_Search_Estimator model is initialized with the provided criterion and shape arguments. 
  If you have already searched the feature extraction module , you can customize the network structure 
  by modifying the `args.feature_operations` parameter. Conversely, if you haven't searched the feature 
  extraction module before, you can use the default conv3 feature extraction we provide.


# Search for the entire network

`--arch_tag 2`

  when arch_tag is set to 2, it indicates that we are performing a comprehensive search across the 
  entire network.The Network_Search_all model is instantiated with the supplied criterion, 
  'Concat_Cell_arc' (denoting a particular type of cell), and shape parameters.


# Conduct training without searching

`--arch_tag 3`

  when arch_tag is set to 3, it indicates that we are exclusively training the network without conducting 
  a search. The Deformable model is initialized with the provided criterion, shape, and the specified 
  operations for both feature extraction and deformation estimation modules, which are given through args. 
  If you have searched the feature extraction and deformation estimation modules before, you can customize 
  your network by modifying the `args.feature_operations` and `args.estimator_operations` parameters. If 
  you want to skip the search and just start training, you can also leave these two parameters undefined 
  and the network will use the default conv3 network we provide.


# How to get searched network models

To obtain the searched network model, you can navigate to the custom output path you specified (Defined by 
the model_path parameter) and locate the log.txt file. In this file, You might see output like this:

`genotype = Genotype(arch=['dil_conv_5x5', 'conv_1x1', 'sep_conv_5x5', 'dil_conv_5x5', 'sep_conv_3x3', 'sep_conv_3x3'])`

This represents the searched model result. Simply copy this line and paste it after the corresponding feature_operations or estimator_operations parameter in your subsequent training process (Note: Please 
delete the `,` between the elements). This will apply the searched network structure to your training.


# Search hyper parameters

It is much easier to search for hyperparameters. Simply add the `--search_hyper` parameter when running the 
command, and the training program will automatically seek the optimal hyperparameters. If your data does 
not include segmentation maps, you should run the train_src_hyper.py file. On the other hand, if your data 
includes segmentation maps, then you should use the train_src_hyper_seg.py file."


# How to get searched hyper parameters

To obtain the searched hyper parameters, you can navigate to the custom output path you specified (Defined by 
the model_path parameter) and locate the log.txt file. In this file, You might see output like this:

  `hyper1 of 048 epoch : 10.000000`
  `hyper2 of 048 epoch : 15.000000`
  `hyper3 of 048 epoch : 3.200000`
  `hyper4 of 048 epoch : 0.800000`

This represents the searched hyper parameters result. If you wish to test the model using the trained
hyperparameters, you can record the values for the four hyperparameters and replace the numerical 
values in `--hyper_parameters 10,15,3.2,0.8` with the values you obtained during training. This will 
apply the searched hyper parameters to your training.


# test

You can run `test.py` to evaluate your training results. You can customize the network architecture using `feature_operations` and `estimator_operations` parameters. If you don't provide custom network structures, 
you can use the default conv3 deformation estimation we provide. Additionally, you can test with discovered 
hyper parameters. We provide a default list of hyper parameters [10, 15, 3.2, 0.8]. If you want to customize 
the hyper parameters, you can modify the value of the hyper_parameters parameter in the command.