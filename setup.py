
from setuptools import setup, find_packages
import pydeconz

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pydeconz",
    version=pydeconz.__version__,
    description=pydeconz.__doc__,
    url=pydeconz.__url__,
    author=pydeconz.__author__,
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