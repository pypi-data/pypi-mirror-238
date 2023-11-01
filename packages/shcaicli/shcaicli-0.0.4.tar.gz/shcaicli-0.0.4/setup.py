from setuptools import setup, find_packages
import os

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="shcaicli",
    version=os.getenv("RELEASE_VERSION"),
    author="iHealth Group",
    author_email="rafael.morais@ihealthgroup.com.br",
    description="SHC.Ai Cli",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.ihealthgroup.com.br",
    project_urls={
        "Bug Tracker": "https://github.com/ihealth-group/shcai-cli/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "antlr4-python3-runtime==4.13.1",
        "requests==2.31.0"
    ],
)
