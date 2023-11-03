from setuptools import setup, find_packages

setup(
    name='sc-common-interface',
    version='1.0',
    description='SC公用的接口',
    author='river',
    packages=find_packages(),
    install_requires=[
    "requests>=2.0.0",

             ],
)
