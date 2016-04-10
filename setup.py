#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dwf',
    version='0.1.0',
    description="Digilent's DWF library wrapper",
    long_description=long_description,
    url='https://github.com/amuramatsu/dwf/',
    author='MURAMATSU Atsushi',
    author_email='amura@tomato.sakura.ne.jp',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6', # Not tested
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3', # Not tested
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',        
    ],
    py_modules=['dwf'],
)
