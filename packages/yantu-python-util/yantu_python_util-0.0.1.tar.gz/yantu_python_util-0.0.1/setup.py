#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunhb
# datetime： 2023/11/2 下午4:32 
# ide： PyCharm
# filename: setup.py.py
import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="yantu_python_util",
  version="0.0.1",
  author="sunhb",
  author_email="598924626@qq.com",
  description="yantu python operate util",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/pypa/sampleproject",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)