# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from testios import __version__, __description__

try:
    long_description = open(os.path.join('testios', "README.md"), encoding='utf-8').read()
except IOError:
    long_description = ""

setup(
    name="testios",
    version=__version__,
    description=__description__,
    author="杨康",
    author_email="772840356@qq.com",
    url="https://gitee.com/bluepang2021/testios",
    platforms="IOS",
    packages=find_packages(),
    long_description=long_description,
    python_requires='>=3.9',
    classifiers=[
        "Programming Language :: Python :: 3.9"
    ],
    include_package_data=True,
    package_data={
        r'': ['*.yml'],
    },
    install_requires=[
        'requests-toolbelt==0.10.1',
        'jmespath==0.9.5',
        'jsonschema==4.17.0',
        'pytest==6.2.5',
        'pytest-rerunfailures==10.2',
        'pytest-xdist==2.5.0',
        'allure-pytest==2.9.45',
        'click~=8.1.3',
        'loguru==0.7.0',
        'urllib3==1.26.15',
        'PyYAML~=6.0',
        'tidevice==0.6.1',
        'facebook-wda==1.4.6',
        'opencv-python==4.6.0.66',
        'filelock==3.12.2'
    ],
    entry_points={
        'console_scripts': [
            'testios = testios.cli:main'
        ]
    }
)
