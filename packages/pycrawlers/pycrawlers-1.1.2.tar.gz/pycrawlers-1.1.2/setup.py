# -*- coding: UTF-8 -*-
# @Time : 2022/8/17 16:07 
# @Author : 刘洪波

import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pycrawlers',
    version='1.1.2',
    packages=setuptools.find_packages(),
    url='https://gitee.com/maxbanana',
    license='Apache',
    author='hongbo liu',
    author_email='782027465@qq.com',
    description='A collection of Crawlers',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'requests>=2.27.1',
        'tqdm>=4.64.0',
        'lxml>=4.8.0',
        'pymongo>=3.12.0',
        'pytz>=2021.3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
