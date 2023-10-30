#This is what your ‘setup.py’ file should look like.
 
from setuptools import setup, find_packages
 
setup(
    name="nostop", #Name
    version="0.0.2", #Version
    packages = find_packages()  # Automatically find the packages that are recognized in the '__init__.py'.
)