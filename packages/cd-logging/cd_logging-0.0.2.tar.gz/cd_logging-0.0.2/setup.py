from setuptools import setup, find_packages
from cd_logging.version import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cd_logging",
    version=__version__,
    author="Code Docta",
    author_email="codedocta@gmail.com",
    description="A simple logging utility for Python applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
url='https://codedocta.com',
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    project_urls={
        'Bug Reports': 'https://github.com/codedocta/CD_HTTP/issues',  # Replace with your issues URL
        'Source': 'https://github.com/codedocta/CD_HTTP/',  # Replace with your repository URL
    },
)


