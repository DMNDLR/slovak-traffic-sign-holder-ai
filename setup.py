#!/usr/bin/env python3
"""
Setup script for Slovak to Czech Article Translator
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="slovak-czech-article-translator",
    version="1.0.0",
    author="Viktor Labovský",
    author_email="labovskyviktor@gmail.com",
    description="Professional Slovak to Czech article translator with HTML preservation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/labovskyviktor-design/slovak-czech-article-translator",
    py_modules=["article_translator"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: Other/Proprietary License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "slovak-czech-translator=article_translator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt"],
    },
)