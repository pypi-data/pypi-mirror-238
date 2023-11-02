import re
import pathlib
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# run setup
setuptools.setup(
    name="MultiPropReg",
    version='0.1',
    license='MIT',
    description="Image registration network using deformation field",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Co-Yonaka/MultiPropReg',
    keywords=['deformation', 'registration', 'imaging', 'mri'],
    package_dir={'MultiPropReg':'MultiPropReg'},
    package_data={'MultiPropReg':['*.*','data/*','models/*','scripts/*','torch/*','pynd/*']},
    # packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5.5',
    install_requires=[
        'packaging',
        'numpy',
        'scipy',
        'nibabel',
    ]
)
