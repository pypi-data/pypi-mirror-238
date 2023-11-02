from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='swebench',
    version='0.2',
    packages=find_packages(),
    install_requires=requirements,
)
