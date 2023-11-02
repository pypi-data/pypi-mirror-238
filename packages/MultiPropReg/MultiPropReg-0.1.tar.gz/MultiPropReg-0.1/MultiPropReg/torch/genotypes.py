from collections import namedtuple

Genotype = namedtuple('Genotype', 'arch')
Genotype_all = namedtuple('Genotype_all', 'normal_fea normal_op')

PRIMITIVES = [
    'conv_1x1',
    'conv_3x3',
    'conv_5x5',
    'sep_conv_3x3',
    'sep_conv_5x5',
    'dil_conv_3x3',
    'dil_conv_5x5',
    'dil_conv_7x7',
]

MR_30epoch = Genotype(arch=['conv_3x3', 'conv_5x5', 'sep_conv_3x3', 'sep_conv_5x5', 'sep_conv_5x5', 'dil_conv_3x3_8'])
