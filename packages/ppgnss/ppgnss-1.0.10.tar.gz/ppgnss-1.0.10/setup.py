# -*- coding: utf-8 -*-
'''
Setup script of ppgnss
'''

from setuptools import setup, find_packages

# python3 setup.py sdist bdist_wheel
# python3 -m twine upload dist/*
# python3 -m twine upload --repository testpypi dist/* # testpypi

setup(
    name='ppgnss',
    version='1.0.10',
    description='Python Package of GNSS data processing',
    # long_description=README,
    author='Liang Zhang',
    author_email='lzhang2019@whu.edu.cn',
    url='https://gitee.com/snnugiser/pygnss',
    # license=LICENSE,
    packages=find_packages(exclude=('tests', 'docs'))
)

