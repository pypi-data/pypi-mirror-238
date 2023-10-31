from setuptools import setup, find_packages

setup(
    name="arzen",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[],
    author="Arzen Tools",
    author_email="code@arzen.sh",
    description="Utilities for CLI apps for Arzen",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
