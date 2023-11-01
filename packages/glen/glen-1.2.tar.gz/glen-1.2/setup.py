# setup.py

from setuptools import setup, find_packages

setup(
    name='glen',
    version='1.2',
    packages=find_packages(),
    install_requires=[
        "torch>=1.13.1",
        "transformers>=4.30.2",
        "pytorch-transformers>=1.2.0"
    ],
)
