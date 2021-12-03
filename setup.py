import os
import setuptools
from setuptools import setup, find_packages

setup(
    name="kvcache",
    version="0.0.1",
    description="Python tool for caching stuff locally",
    python_requires=">=3.4",
    author="Adam Frank",
    author_email="pkgmaint@antilogo.org",
    packages=find_packages(),
    project_urls={"Source": "https://github.com/afrank/kvcache",},
)

