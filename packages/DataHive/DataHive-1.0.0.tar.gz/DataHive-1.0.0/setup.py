from setuptools import setup, find_packages
import codecs
import os

# Get the current directory
here = os.path.abspath(os.path.dirname(__file__))

# Read the README file as long description
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'DataHive is a Python library and tool for managing and querying JSON-based file system databases (FSDB). ' \
              'It provides a simple and efficient way to work with structured data stored in JSON format on your ' \
              '-mlocal file system. '


# Define the authors
author_name_2 = 'Yahya Azzam'
author_email_2 = 'yahya912azzam@gmail.com'
author_name_1 = 'Mahmoud Goda'
author_email_1 = 'mahmoden17@gmail.com'

# Combine author information
authors = f"{author_name_1} <{author_email_1}>, {author_name_2} <{author_email_2}>"

# Setting up
setup(
    name="DataHive",
    version=VERSION,
    author=authors,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    package_data={'DataHive': ['*.json', '*.py']},
    include_package_data=True,
    license="MIT",
    entry_points={
        "console_scripts": ['DataHive = DataHive.__main__:main']
    },
    url="https://github.com/YahyaAzzam/SimpleFSDB",
    python_requires='>=3.5',
    install_requires=[
        "argparse>=1.4.0",
        "pathlib>=1.0.1",
        "uuid>=1.30",
    ],
    keywords=['DB', 'json', 'DataHive', 'File System', 'FSDB', 'simpleFSBD', 'SFSDB'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
