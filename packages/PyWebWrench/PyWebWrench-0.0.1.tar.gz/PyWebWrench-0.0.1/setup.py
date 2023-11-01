from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="PyWebWrench",
    version="0.0.1",
    description="PyWebWrench is a Python library that enables you to view web pages and make HTTP requests",
    author="09u2h4n",
    author_email="09u2h4n.y1lm42@gmail.com",
    packages=find_packages(),
    install_requires=["requests", "playwright"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Source Code": "https://github.com/09u2h4n/pyapks",
        "Author's Github": "https://github.com/09u2h4n"
    }
)