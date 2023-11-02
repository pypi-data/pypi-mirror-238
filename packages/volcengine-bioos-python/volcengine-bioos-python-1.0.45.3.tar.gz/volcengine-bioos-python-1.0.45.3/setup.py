# coding: utf-8

from setuptools import setup, find_packages  # noqa: H301

NAME = "volcengine-bioos-python"
VERSION = "1.0.45.3"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "certifi",
    "python-dateutil>=2.1",
    "six>=1.10",
    "urllib3>=1.23"
]

setup(
    name=NAME,
    version=VERSION,
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    description='Volcengine Bio2s SDK for Python',
    license="Apache License 2.0",
    platforms='any',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/volcengine/volcengine-python-sdk',
)
