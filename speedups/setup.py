#!/usr/bin/env python
import sys
sys.path.insert(0, '..')

from distutils.core import setup
from distutils.extension import Extension

from pymorphy_speedups.version import __version__

setup(
    name = 'pymorphy-speedups',
    version = __version__,
    author = 'Mikhail Korobov',
    author_email = 'kmike84@gmail.com',

    description = 'Speedups for pymorphy',
    long_description = open('README.rst').read(),

    ext_modules = [Extension("pymorphy_speedups._morph", ["_morph.c"])],

    license = 'MIT license',
    packages = ['pymorphy_speedups'],
    requires = ['pymorphy (==%s)' % __version__],

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
