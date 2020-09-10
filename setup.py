#!/usr/bin/env python3
import re
from os import path

from setuptools import find_packages, setup

curpath = path.abspath(path.dirname(__file__))
with open(path.join(curpath, "README.md")) as f:
    long_description = f.read()


def read(*parts):
    with open(path.join(curpath, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='sjtu_schedule_exporter_cli',
    version=find_version("sjtu_schedule_exporter_cli", "__init__.py"),
    description='A simple utility to export your SJTU schedule in ICS format',
    author='LightQuantum',
    author_email='self@lightquantum.me',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url='https://github.com/PhotonQuantum/sjtu-schedule-exporter-cli',
    classifiers=(
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ),
    install_requires=[
        'pysjtu',
        'blessed',
        'ics',
        'arrow<0.15'
    ],
    entry_points={
        'console_scripts': [
            "sjtu-schedule-exporter-cli=sjtu_schedule_exporter_cli.__main__:main"
        ]
    }
)
