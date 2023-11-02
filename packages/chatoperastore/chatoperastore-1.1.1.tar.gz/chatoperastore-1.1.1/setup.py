# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
LONGDOC = """
# Chatopera Store SDK for Python

Chatopera 证书商店 Python SDK

https://store.chatopera.com

"""

setup(
    name='chatoperastore',
    version='1.1.1',
    description='Chatopera Store SDK for Python, Chatopera 证书商店 Python SDK, 实现软件中付费资源的证书管理，比如检查配额、证书验证、续费管理等',
    long_description=LONGDOC,
    long_description_content_type="text/markdown",
    author='Hai Liang Wang',
    author_email='hain@chatopera.com',
    url='https://store.chatopera.com',
    license="Chunsong Public License, version 1.0",
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Chinese (Traditional)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='billing,invoice,payment,license',
    packages=find_packages(),
    install_requires=[
    ],
    package_data={
        'chatoperastore': ['LICENSE']}
)
