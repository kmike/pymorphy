#!/usr/bin/env python
from distutils.core import setup
import sys

for cmd in ('egg_info', 'develop', 'build_sphinx', 'upload_sphinx'):
    if cmd in sys.argv:
        from setuptools import setup

setup(
    name = 'pymorphy',
    version=__import__('pymorphy').__version__,
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',
    url='http://bitbucket.org/kmike/pymorphy/',
    download_url = 'http://bitbucket.org/kmike/pymorphy/get/tip.zip',

    description = 'Morphological analyzer for Russian and English (+perhaps German) languages.',
    long_description = open('README').read() + open('docs/CHANGES.rst').read(),

    license = 'MIT license',
    packages = ['pymorphy',
                'pymorphy.contrib',
                'pymorphy.backends',
                'pymorphy.backends.shelve_source',
                'pymorphy.templatetags'],

    classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: Russian',
          'Natural Language :: English',
          'Natural Language :: German',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Framework :: Django',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Text Processing :: Linguistic',
    ],
)
