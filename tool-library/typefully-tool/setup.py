#!/usr/bin/env python3
"""Setup script for Typefully CLI."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="typefully-cli",
    version="0.1.0",
    author="Pete",
    description="Command-line interface for Typefully API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pete/tool-library/typefully-tool",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Communications",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "typefully=typefully_cli:cli",
        ],
    },
)