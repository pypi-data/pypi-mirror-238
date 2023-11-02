from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pikmin",
    version="6.9",
    author="Masti Khor",
    author_email="arpitsengar99@gmail.com",
    description="package for playing pikmin from the cli.",
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
    package_data={'pikmin': ['assets/*.wav']},
    include_package_data=True
)