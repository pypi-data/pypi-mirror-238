from setuptools import setup

__project__ = "malware_examples"
__version__ = "0.0.1"
__description__ = "a few basic examples of malware along with decryptors"
__packages__ = ["malware_example"]
__author__ = "Abhimanyu Daripally"
__author_email__ = "abhi.cl9898@gmail.com"
__classifiers__ = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Education",
    "Programming Language :: Python :: 3.11",
    "License :: Free for non-commercial use",
    "Natural Language :: English",
    "Operating System :: Other OS",
    
    
]
__requires__ = ["os", "cryptography", "sys"]

setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    author_email = __author_email__,
    classifiers = __classifiers__,
    requires = __requires__,
    
)
