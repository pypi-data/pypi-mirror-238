#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Cai Jianping
# Mail: jpingcai@163.com
# Created Time:  2023-4-29 07:13:42
#############################################


from setuptools import setup, find_packages
#主要变量
name="efpy"
version = "0.1.16"
install_requires = ['PyYAML']

setup(
    name = name,
    version = version,
    keywords = ("experience","environment"),
    description = "experience",
    long_description = "experience",
    license = "MIT Licence",

    url = "https://github.com/imcjp/efpy",
    author = "Cai Jianping",
    author_email = "jpingcai@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = install_requires
)
