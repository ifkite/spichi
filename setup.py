import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def readlines(fname):
    contents = open(os.path.join(os.path.dirname(__file__), fname)).readlines()
    return [name.strip() for name in contents]

setup(
    name = "spichi",
    version = "0.0.9",
    author = "ifkite",
    author_email = "holahello@163.com",
    description = ("a web framework"),
    license = "MIT",
    keywords = "web-framework",
    url = "https://github.com/ifkite/spichi",
    packages=find_packages(exclude=['tests', 'examples', 'build', 'dist', 'spichi.egg-info']),
    install_requires=readlines('requirements.txt'),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Planning",
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License'
    ],
)
