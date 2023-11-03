from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='code_wallet',
    version='1.0.4',
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    long_description=long_description,
    long_description_content_type="text/markdown",
)