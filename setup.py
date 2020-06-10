
from setuptools import setup, find_packages


__version__ = "0.9.8"
__author__ = "balu-"
__url__ = "https://github.com/balu-/deconzpy"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="deconzpy",
    version=__version__,
    description=__doc__,
    url=__url__,
    author=__author__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(exclude=['testing']),
    keywords='deconz zigbee homeautomation',
    install_requires=['requests', 'websocket-client'],
)