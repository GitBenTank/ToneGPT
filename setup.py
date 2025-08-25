#!/usr/bin/env python3
"""
🎸 ToneGPT AI - Setup Configuration

AI-powered FM9 tone generation platform setup and installation.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read version from package
exec(open("tonegpt/__init__.py").read())

setup(
    name="tonegpt-ai",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="AI-powered tone generation platform for Fractal Audio FM9",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=__url__,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.28.0",
        "numpy>=1.21.0",
        "plotly>=5.0.0",
        "RapidFuzz>=3.13.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
        "audio": [
            "librosa>=0.9.0",
            "scipy>=1.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tonegpt=tonegpt.interface.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "tonegpt": [
            "core/*.json",
            "*.json",
        ],
    },
    keywords=[
        "guitar", "tone", "ai", "fm9", "fractal", "audio", "music", "generation"
    ],
    project_urls={
        "Bug Reports": f"{__url__}/issues",
        "Source": __url__,
        "Documentation": f"{__url__}/blob/main/README.md",
    },
)
