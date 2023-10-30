from setuptools import setup, find_packages

setup(
    name="vectorflow-client",
    version="0.0.1",
    packages=find_packages() + ['shared'],
    package_dir={'shared': '../src/shared'},
    install_requires=[
        'requests==2.31.0'
    ],
)
