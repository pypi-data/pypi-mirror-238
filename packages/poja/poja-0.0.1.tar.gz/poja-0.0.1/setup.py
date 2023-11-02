from setuptools import setup, find_packages
from poja.version import get_version


def get_long_description():
    with open("README.md", "r") as readme:
        return readme.read()


setup(
    name="poja",
    version=get_version(),
    description="Serverless Postgres+Java hosted on Github+AWS",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="HEI",
    author_email="contact@hei.school",
    url="https://github.com/hei-school/poja-cli",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
)
