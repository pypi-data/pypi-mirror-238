# -*- coding: utf-8 -*-
"""
@author: deiro
"""
from setuptools import setup

setup(
    name='ThunderFlowPro',
    version='0.1.0',
    description='Consumption estimation EV battery',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Andres Cordeiro',
    author_email='cordeiroandres@gmail.com',
    url='https://github.com/cordeiroandres/EV-battery-calculator',
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
        'rasterio>=1.2.10'
    ],
    python_requires=">=3.8.13",
)
