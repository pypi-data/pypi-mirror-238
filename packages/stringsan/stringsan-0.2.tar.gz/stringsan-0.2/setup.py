from setuptools import setup, find_packages
import stringsan 

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=stringsan.__name__,
    version=stringsan.__version__,
    author=stringsan.__author__,
    author_email=stringsan.__email__,
    description=stringsan.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=stringsan.__repository__,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
