from setuptools import setup, find_packages

# Read the contents of requirements.txt
with open('requirements.txt', 'r', encoding='utf-16') as f:
    requirements = f.read().splitlines()

setup(
    name='growth-ops-apps-common',
    version='1.0.1',
    description='Common utilities for Growth Ops Apps',
    packages=find_packages(),
    install_requires=requirements,
)
