from setuptools import setup, find_packages
from config import email

with open('README.md', encoding='utf-8') as f:
    long_dcs2 = f.read()

version = '0.0.2'
long_dcs = '''This module for create database with JSON'''

setup(
    name = 'database_json',
    version=version,
    author='Hleb2702',
    author_email=email,
    long_description_content_type="text/markdown",
    description=long_dcs,
    long_description=long_dcs2,
    url='https://github.com/hleb2702/json_db.git',

    download_url='https://github.com/hleb2702/json_db/archive/refs/heads/main.zip',

    license='Apache License, Version 2.0, see LICENSE file',
    packages=find_packages(),
    requires=['json']
)


