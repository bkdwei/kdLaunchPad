#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages
import os

desktop_path = os.path.join(os.path.expanduser("~"),"Desktop/kdLaunchPad.bat")
if os.name == 'nt':
    with open(desktop_path,"w",encoding="utf-8") as shotcut:
        shotcut.write(("echo hi").encode(coding="utf-8"))
        
with open("kdLaunchPad/README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setup(
#     固定部分
    name="kdLaunchPad",
    version="1.0.3",
    author="bkdwei",
    author_email="bkdwei@163.com",
    maintainer="韦坤东",
    maintainer_email="bkdwei@163.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bkdwei/kdLaunchPad",
    license="GPLv3+",
    platforms=["Windows", "Linux"],
    # 需要安装的依赖
    install_requires=["PyQt5"],
    packages=find_packages(),
    package_data={"":["*","image/*"],},
    zip_safe=False,

#     可变部分
    description="auto run some programs after system start",
    keywords=("kdLaunchPad","autoStarter"),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Developers",
        "Natural Language :: Chinese (Simplified)",
        "Topic :: Software Development :: Documentation",
        "Programming Language :: Python :: 3",
        " License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        
    ],
    
     # 添加这个选项，在windows下Python目录的scripts下生成exe文件
     # 注意：模块与函数之间是冒号:
    entry_points={
        'console_scripts': [
            'kdLaunchPad=kdLaunchPad.kdLaunchPad:main'
        ],    
    }
)