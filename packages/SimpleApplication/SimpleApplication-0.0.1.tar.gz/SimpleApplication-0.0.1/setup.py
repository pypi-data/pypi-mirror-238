from setuptools import setup, find_packages
import os

requirements_path = "requirements.txt"

with open(requirements_path, "r") as f:
    dependencies = f.read().splitlines()

setup(
    name="SimpleApplication",
    version="0.0.1",
    description="Simple Application in Python",
    url='https://gitlab.com/carrivalegervasi/2023_assignment1_carrigerva.git',
    author="CarrivaleGervasi",
    packages=find_packages(), 
    install_requires=dependencies,
)
