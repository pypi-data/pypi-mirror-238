from setuptools import setup
import os

# The path to the requirements.txt file.
requirements_path = os.path.join("urluckynum", "requirements.txt")

# Read the dependencies from the requirements.txt file.
with open(requirements_path, "r") as f:
    dependencies = f.read().splitlines()

# Specify the package structure.
setup(
    name='urluckynum', # The name of the package.
    version='9.32', # The version of the package.
    description='My Application with a DB', # A short description of the package.
    author='LuckyWave Group', # The author of the package.
    packages=[ # A list of the packages in the package.
        'urluckynum.app',
    ],
    package_dir={ # A dictionary that maps package names to directories.
        'urluckynum': 'urluckynum',
    },
    install_requires=dependencies, # List of the dependencies that the package requires.
) 