from setuptools import find_packages, setup

setup(
    name='dams_extractor',
    author='Brian Scherzo',
    version='0.2',
    description='A boilerpy3 text extractor wrapper',
    long_description='A wrapper for NumWordsRule boilerpy3 text extraction.  Made for use by the UMBC DAMS Lab.',
    packages=find_packages(),
    zip_safe=False
)