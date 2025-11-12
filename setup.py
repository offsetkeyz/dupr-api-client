"""Setup script for dupr-api-client."""

from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dupr-api-client",
    version="1.0.0",
    author="offsetkeyz",
    author_email="pypi@thedailydecrypt.com",
    description="A comprehensive Python client library for the DUPR API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/offsetkeyz/dupr-api-client",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*", "docs", "docs.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "responses>=0.23.0",
            "black>=23.7.0",
            "mypy>=1.5.0",
            "flake8>=6.1.0",
            "types-requests>=2.31.0",
        ],
    },
    keywords="dupr pickleball rating api client",
    project_urls={
        "Bug Tracker": "https://github.com/offsetkeyz/dupr-api-client/issues",
        "Documentation": "https://github.com/offsetkeyz/dupr-api-client#readme",
        "Source Code": "https://github.com/offsetkeyz/dupr-api-client",
    },
)
