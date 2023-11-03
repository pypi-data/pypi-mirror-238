# Author: Kenta Nakamura <c60evaporator@gmail.com>
# Copyright (c) 2020-2021 Kenta Nakamura
# License: BSD 3 clause

from setuptools import setup
import intlab

DESCRIPTION = "IISL: SAP-net"
NAME = 'intlab'
AUTHOR = 'Sora Takaya'
AUTHOR_EMAIL = 'so12ra16@outlook.jp'
URL = 'https://github.com/takayasora/intlab'
LICENSE = 'MIT License'
DOWNLOAD_URL = 'https://github.com/takayasora/intlab'
VERSION = intlab.__version__
PYTHON_REQUIRES = ">=3.6"

INSTALL_REQUIRES = [
    'pandas>=1.2.4'
]

EXTRAS_REQUIRE = {
    'tutorial': [
        'mlxtend>=0.18.0'
    ]
}

PACKAGES = [
    'intlab'
]

CLASSIFIERS = [
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License',
]

with open('README.rst', 'r') as fp:
    readme = fp.read()
    
long_description = readme 

setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description=long_description,
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE,
      packages=PACKAGES,
      classifiers=CLASSIFIERS
    )
