# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 20:36:58 2017

@author: a
"""
version='0.1.0'
package='seed_cluster'

from setuptools import setup, Extension
import os,io

c=['seed_cluster.c']

# with io.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'),encoding='utf-8') as f:
#     long_description = f.read()
setup(
    #基本信息
    name = package,
    version = version,
    keywords = ("seed_cluster"),
    description = "seed_cluster",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url = "",  
    author = "",
    author_email = "",
    
    #协议
    license = "Licence",
    
    #环境依赖
    platforms = "any",
    
    install_requires = [],

    #打包范围
    ext_modules=[Extension(i.replace('.c','').replace('/','.'),sources=[i]) for i in c],
    )

#python setup.py bdist_wheel -universal
#python setup.py sdist