from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pikmin",
    version="1.2",
    author="Arpit Sengar",
    author_email="arpitsengar99@gmail.com",
    description="A Python package for playing pikmin from the command line.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arpy8/pikmin",
    packages=find_packages(),
    install_requires=["pygame"],
    entry_points={
        "console_scripts": [
            "pikmin=pikmin.player:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
