# Copyright 2023 Hao Hoang (haohoangofficial@gmail.com)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os

this_dir = os.path.dirname(__file__)
readme_filename = os.path.join(this_dir, 'README.md')
requirements_filename = os.path.join(this_dir, 'requirements.txt')

PACKAGE_NAME = 'responsinator'
PACKAGE_VERSION = '1.0.1'
PACKAGE_AUTHOR = 'Hao Hoang'
PACKAGE_AUTHOR_EMAIL = 'haohoangofficial@gmail.com'
PACKAGE_URL = 'https://github.com/hdsme/responsinator'
PACKAGE_DOWNLOAD_URL = \
    'https://github.com/hdsme/responsinator/tarball/' + PACKAGE_VERSION
PACKAGES = [
    'responsinator'
]
PACKAGE_DATA = {
    'responsinator': ['*.crt'],
    'responsinator.test': ['*.jpg']
}
PACKAGE_LICENSE = 'LICENSE.txt'
PACKAGE_DESCRIPTION = 'HTTP Response SDK'

with open(readme_filename) as f:
    PACKAGE_LONG_DESCRIPTION = f.read()

with open(requirements_filename) as f:
    PACKAGE_INSTALL_REQUIRES = [line[:-1] for line in f]

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author=PACKAGE_AUTHOR,
    author_email=PACKAGE_AUTHOR_EMAIL,
    url=PACKAGE_URL,
    download_url=PACKAGE_DOWNLOAD_URL,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    license=PACKAGE_LICENSE,
    description=PACKAGE_DESCRIPTION,
    long_description=PACKAGE_LONG_DESCRIPTION,
    install_requires=PACKAGE_INSTALL_REQUIRES,
    long_description_content_type="text/markdown",
)
