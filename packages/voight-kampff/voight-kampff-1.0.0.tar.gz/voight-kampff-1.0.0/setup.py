"""Setup script for package."""
# pylint: disable=consider-using-with,no-self-use
import os
import re
import sys

from setuptools import Command, find_packages, setup

match = re.search(
    r'^VERSION\s*=\s*"(.*)"',
    open("voight_kampff/version.py", encoding="utf_8").read(),
    re.M,
)

VERSION = match.group(1) if match else "???"
with open("README.md", "rb") as f:
    LONG_DESCRIPTION = f.read().decode("utf-8")


class VerifyVersion(Command):
    """Command for verifying that git tag matches package version."""

    description = "verify that the git tag matches package version"
    user_options = []

    def initialize_options(self):
        """Implement required method for Command."""

    def finalize_options(self):
        """Implement required method for Command."""

    def run(self):
        """
        Check that the git tag matches the package version.

        If it doesn't match, exit.
        """
        tag = os.getenv("CIRCLE_TAG")
        if not _validate_version(tag, VERSION):
            info = f"Git tag: '{tag}' does not match package version: {VERSION}"
            sys.exit(info)


def _validate_version(tag: str | None, version: str) -> bool:
    if not tag:
        return version == "0.0.0"
    if tag[0] != "v":
        return False
    return tag[1:] == version


setup(
    name="voight-kampff",
    version=VERSION,
    description="Simple command line app for running Python linters.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Soren Kristiansen",
    author_email="soren@gutsandglory.dk",
    url="https://github.com/sorenlind/voight-kampff/",
    keywords="",
    packages=find_packages(),
    install_requires=[
        "black",
        "flake8",
        "isort",
        "pyenchant",
        "pylint",
    ],
    extras_require={
        "dev": [
            "coverage",
            "flake8-annotations",
            "flake8-bandit",
            "flake8-docstrings",
            "flake8-plus",
            "flake8-pytest-style",
            "pytest-cov",
            "pytest-mock",
            "pytest",
            "rope",
            "tox",
        ],
        "test": [
            "coverage",
            "pytest-cov",
            "pytest-mock",
            "pytest",
            "tox",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
    ],
    cmdclass={
        "verify": VerifyVersion,
    },
    entry_points={
        "console_scripts": [
            "vk = voight_kampff.__main__:main",
        ]
    },
)
