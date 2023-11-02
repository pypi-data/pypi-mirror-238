from setuptools import setup, find_packages

setup(
    name="calculator_james",
    version="0.1.0",
    author="James",
    author_email="james.chang@cerence.com",
    description="A small test example package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://git.labs.hosting.cerence.net/james.chang/pypi_package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)