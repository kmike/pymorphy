#!/usr/bin/env python
from distutils.core import setup
from distutils.extension import Extension

setup(
    name = 'pymorphy-speedups',
    version='0.5.1',
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',

    description = 'Speedups for pymorphy',
    long_description = open('README.rst').read(),

    ext_modules = [Extension("pymorphy_speedups._morph", ["_morph.c"])],

    license = 'MIT license',
    packages = ['pymorphy_speedups'],
    requires = ['pymorphy(>=0.5)'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Natural Language :: German',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ],
)
