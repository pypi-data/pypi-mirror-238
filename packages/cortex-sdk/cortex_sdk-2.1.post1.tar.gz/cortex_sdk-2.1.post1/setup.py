from setuptools import find_packages, setup

# Setup custom import schema
# cortex.__version__
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current)

from cortex import __version__

setup(
    name="cortex_sdk",
    version=__version__,
    packages=find_packages(exclude=['tests*']),
    author='Nearly Human',
    author_email='support@nearlyhuman.ai',
    description='Nearly Human Cortex SDK dependency for interacting with APIs.',
    keywords='nearlyhuman, nearly human, cortex, sdk',

    python_requires='>=3.8.10',
    # long_description=open('README.txt').read(),
    install_requires=[
        'requests>=2.31.0',
        'setuptools'
    ]
)