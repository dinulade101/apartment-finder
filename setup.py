#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()


NAME = 'apartment-finder'
DESCRIPTION = 'Scrapes Kijiji for apartments and finds spec'
URL = 'https://github.com/ahmedelgohary/apartment-finder'
EMAIL = 'elgohary@ualberta.ca'
AUTHORS = 'Ahmed El Gohary & Manimeldura De Silva'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '1.0'

REQUIREMENTS = [
    "BeautifulSoup4", "requests"
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHORS,
    author_email=EMAIL,
    packages=[NAME],
    install_requires=REQUIREMENTS
)
