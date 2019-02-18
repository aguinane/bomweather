""" A setuptools based setup module.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
try:
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''

setup(
    name='bomweather',
    version='0.2.0',
    description=
    'Load weather data from the Australian Bureau of Meteorology (BOM) website',    
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    python_requires='>=3.4',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Alex Guinane',
    author_email='alexguinane@gmail.com',
    url='https://github.com/aguinane/bomweather',
    keywords=['weather', 'bom'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    install_requires=[
        'requests',
        'python-dateutil',
        'pytz',
    ],   
)
