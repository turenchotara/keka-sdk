#!/usr/bin/env python3
"""
Setup script for Keka SDK
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    """Read README.md file for long description"""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Keka SDK - A Python SDK for interacting with the Keka HR API"

# Read version from __init__.py
def get_version():
    """Extract version from keka_sdk/__init__.py"""
    version = {}
    version_path = os.path.join(os.path.dirname(__file__), 'keka_sdk', '__init__.py')
    try:
        with open(version_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('__version__'):
                    exec(line, version)
                    return version['__version__']
    except (FileNotFoundError, KeyError):
        pass
    return "1.0.0"

setup(
    name="keka-sdk",
    version=get_version(),
    author="Turen Chotara",
    author_email="turenchotara7@gmail.com ",
    description="A Python SDK for interacting with the Keka HR API",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/keka-sdk",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/keka-sdk/issues",
        "Source": "https://github.com/yourusername/keka-sdk",
        "Documentation": "https://developers.keka.com/reference"
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Human Resources",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "httpx>=0.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "myst-parser>=1.0.0",
        ]
    },
    keywords=[
        "keka", 
        "hr", 
        "api", 
        "sdk", 
        "human-resources", 
        "payroll", 
        "employee-management",
        "helpdesk",
        "authentication"
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            # Add any command-line tools here if needed
            # "keka-cli=keka_sdk.cli:main",
        ],
    },
)
