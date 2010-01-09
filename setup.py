#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from distutils.core import setup

readme = open(os.path.join(os.path.dirname(__file__), 'README')).read()

setup(
    name     = 'pymorphy',
    version  = '0.4.1',
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',
    url='http://bitbucket.org/kmike/pymorphy/',
    download_url = 'http://bitbucket.org/kmike/pymorphy/get/tip.zip',

    description = 'Morphological analyzer for Russian and English (+perhaps German) languages.',
    long_description = readme,

    license = 'MIT license',
    packages = ['pymorphy',
                'pymorphy.backends',
                'pymorphy.backends.shelve_source',
                'pymorphy.templatetags'],

    requires = ['python (>=2.5)'],

    classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: Russian',
          'Natural Language :: English',
          'Natural Language :: German',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Text Processing :: Linguistic',
    ],
)
