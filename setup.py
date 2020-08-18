#!/usr/bin/env python

from setuptools import setup

setup(
    name="osm-iso3166-grabber",
    version="0.0.1",
    description="Get ISO 3166 data from OpenStreetMap",
    url="https://github.com/pR0Ps/osm-iso3166-grabber",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    py_modules=["iso3166_grabber"],
    entry_points={"console_scripts": ["iso3166-grabber=iso3166_grabber:main"]},
)
