from setuptools import setup, find_packages

setup(
    name="darlehen.py",
    version="0.9",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    author="Michael Peter",
    author_email="michaeljohannpeter@gmail.com",
    description="darlehenpy bietet Funktionen zur Berechnung eines Darlehens",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/allaman/darlehenpy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
