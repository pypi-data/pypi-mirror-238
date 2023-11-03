# -*- coding: utf-8 -*-
"""
@author: deiro
"""
from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='ThunderFlowPro',
    version='0.1.2',
    description='Consumption estimation EV battery',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Andres Cordeiro',
    author_email='cordeiroandres@gmail.com',
    url='https://github.com/cordeiroandres/ThunderFlowPro',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        ],
    packages=['ThunderFlowPro'],
    install_requires=[
        'pandas>=1.5.2',
        'numpy>=1.22.4',        
        'numba>=0.56.4',
        'requests>=2.23.0',        
        'polyline>=1.4.0',
        'rasterio>=1.2.10',
        'meteostat>=1.6.3'
    ],
    python_requires=">=3.8.13",
)
