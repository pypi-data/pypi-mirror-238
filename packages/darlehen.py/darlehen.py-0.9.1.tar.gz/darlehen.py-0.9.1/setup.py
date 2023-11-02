"""Package configuration"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as file:
    long_description = file.read()

setup(
    name="darlehen.py",
    version="0.9.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    author="Michael Peter",
    author_email="michaeljohannpeter@gmail.com",
    description="darlehenpy bietet Funktionen zur Berechnung eines Darlehens",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/allaman/darlehenpy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
