# read the contents of your README file
from pathlib import Path
from mhash import __version__
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="lihash",
    version=__version__,
    author="Moses Dastmard",
    description="hashing strings",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=["hashlib"],
)