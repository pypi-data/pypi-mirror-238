from setuptools import setup, find_packages
from os.path import dirname, join

setup(
    name='ZvolvArithmetic',
    version='0.1.0',
    description='Official Zvolv Arithmetic Python SDK',
    long_description_content_type="text/markdown",
    long_description= open(join('README.md'), encoding='utf-8').read(),  
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
)