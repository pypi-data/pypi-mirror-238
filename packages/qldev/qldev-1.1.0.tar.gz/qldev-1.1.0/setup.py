from setuptools import setup
from setuptools import find_packages

VERSION = '1.1.0'
AUTHOR='eegion'
EMAIL='hehuajun@eegion.com'

option = {
    "build_exe": {
        "excludes":["test", "main"],
        'packages':['utils','network','device','box']
    }
}

setup(
    name='qldev',  # package name
    version=VERSION,  # package version
    author=AUTHOR,
    author_email=EMAIL,
    description='api for quanlan box since v1.2.2',  # package description
    packages=find_packages(),
    install_requires=['loguru', 'numpy'],
    package_data={
        "":["*.txt", "*.md"]
    },
    zip_safe=False
)