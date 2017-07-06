#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

import sys
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dwf',
    version='0.2.0.dev0',
    description="Digilent's DWF library wrapper",
    long_description=long_description,
    url='https://github.com/amuramatsu/dwf/',
    author='MURAMATSU Atsushi',
    author_email='amura@tomato.sakura.ne.jp',
    license='MIT',
    install_requires=[
        'enum34'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6', # Not tested
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3', # Not tested
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',        
    ],
    platforms="Linux,Mac,Windows",
    packages=['dwf'],
    use_2to3=False
)
