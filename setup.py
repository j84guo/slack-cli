from setuptools import setup

"""
distutils - standard tool for packaging python projects, featured in the standard library 
setuptools - heavily favoured third party tool for packaging python projects, not a part of the standard library 
setup.py - canonical script used by both disutils and setuptools to gather the locations of project sources and metadata
egg - python package format originally introduced by setuptools, it is essentially an importable zipped package 
easy_install - python package manager introduced with setuptools which only installs egg packages from PyPI
wheel - officially recommended package format for python projects, can be built with python3 setup.py bdist_wheel and installed with pip3 install dist/<name>.whl
"""

setup(
   name='slack_cli',
   version='1.0',
   description="Command line interface for interacting with Slack's API",
   author='Jackson G',
   author_email='jackson.guo@zerogravitylabs.ca',
   packages=['slack_cli'],
   entry_points={
      'console_scripts': [
         'slk=slack_cli.cli:main',
      ],
   }
)
