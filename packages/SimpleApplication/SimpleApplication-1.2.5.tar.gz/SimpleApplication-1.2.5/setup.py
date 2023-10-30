from setuptools import setup, find_packages
import os

requirements_path = "requirements.txt"

with open(requirements_path, "r") as f:
    dependencies = f.read().splitlines()

setup(
    name="SimpleApplication",
    version="1.2.5",
    description="Simple Application in Python",
    author="CarrivaleGervasi",
    packages=find_packages(), 
    install_requires=dependencies,
)
