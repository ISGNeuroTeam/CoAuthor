from setuptools import find_packages
from setuptools import setup

try:
    with open("requirements.txt") as f:
        requirements = f.readlines()
except:
    requirements = []

setup(
    name="CoAuthor",
    description="Application for analysis and creation news",
    version="0.1.0",
    packages=find_packages(),
    url="https://github.com/ISGNeuroTeam/CoAuthor",
    install_requires=requirements,
    options={"bdist_wheel": {"universal": 1}},
)
