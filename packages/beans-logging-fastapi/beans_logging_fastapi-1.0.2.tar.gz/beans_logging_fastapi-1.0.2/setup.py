# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from distutils.util import convert_path


_package_name = "beans_logging_fastapi"

_namespace_dict = {}
_version_path = convert_path(f"{_package_name}/__version__.py")
with open(_version_path) as _version_file:
    exec(_version_file.read(), _namespace_dict)
_package_version = _namespace_dict["__version__"]

setup(
    name=_package_name,
    packages=find_packages(),
    version=f"{_package_version}",
    license="MIT",
    description=f"'{_package_name}' is a middleware for FastAPI to log HTTP access. It is based on 'beans-logging' package.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="Batkhuu Byambajav",
    author_email="batkhuu10@gmail.com",
    url="https://github.com/bybatkhuu/module.fastapi-logging",
    download_url=f"https://github.com/bybatkhuu/module.fastapi-logging/archive/v{_package_version}.tar.gz",
    keywords=[
        _package_name,
        "fastapi-logging",
        "fastapi-logging-middleware",
        "fastapi-middleware",
        "logging-middleware",
        "middleware",
        "beans-logging",
        "http-access-logging",
        "logging",
        "logger",
        "loguru",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.99.1,<1.0.0",
        "beans-logging>=6.0.0,<7.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
