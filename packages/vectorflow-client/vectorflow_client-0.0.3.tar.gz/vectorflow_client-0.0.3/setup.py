from setuptools import setup, find_packages

# Read the content of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vectorflow_client",
    version="0.0.3",
    packages=find_packages(),
    install_requires=[
        'requests==2.31.0'
    ],
    include_package_data=True,  # This is the line that reads the MANIFEST.in
    long_description=long_description,
    long_description_content_type="text/markdown",
)
