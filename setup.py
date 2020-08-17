# coding: utf-8
from ffd.__version__ import __version__
import setuptools


setuptools.setup(
  name='amid3',
  version=__version__,
  author='dlr',
  author_email='dlr@yy.com',
  description=u'm4a ID3 editor',
  packages=setuptools.find_packages(),
  url='https://dlran.github.io',
  entry_points={
    'console_scripts': [
      'amid3=amid3.cli:main'
    ]
  },
  classifiers=[
      'Programming Language :: Python :: 3 :: Only'
  ]
)
