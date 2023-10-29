from setuptools import setup, find_packages
from labnotebook import __version__
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pylabnotebook',
    version=__version__,
    description="This package provides functions to write an automated labnotebook using git.",
    long_description=long_description,
    long_description_content_type='text/markdown',

    author="Matteo Miotto",
    author_email="miotsdata@gmail.com",
    
    packages=find_packages(),
    package_data={'labnotebook': ['templates/*']},
    entry_points={
        'console_scripts': [
            'labnotebook = labnotebook.main:main',
        ],
    },
    install_requires=[
        "argparse",
    ],
)
