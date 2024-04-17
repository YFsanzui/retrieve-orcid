# setup.py
from setuptools import setup

def get_requirements():
    with open("./requirements.txt") as f_in:
        requirements = f_in.read().splitlines()
    return requirements

setup(
    install_requires=get_requirements()
    )
