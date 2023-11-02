from setuptools import setup

# Read the contents of requirements.txt
with open('requirements.txt', 'r', encoding='utf-16') as f:
    requirements = f.read().splitlines()

setup(
    name='growth-ops-apps-common',
    version='1.0',
    description='Common utilities for Growth Ops Apps',
    packages=['common'],
    install_requires=requirements,
)
