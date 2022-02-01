from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="medstone_backend",
    version="1.0.0",
    url="https://datastem.nl",
    author="Koen Vijverberg",
    author_email="koen@vijverb.nl",
    description="A REST API",
    packages=find_packages(exclude=("tests",)),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7"
    ],
)
