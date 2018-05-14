from setuptools import setup

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
