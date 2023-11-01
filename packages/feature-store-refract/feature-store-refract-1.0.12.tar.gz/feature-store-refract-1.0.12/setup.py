# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

extras_require = {
    "feast": []
}

setup(
    name="feature-store-refract",
    version="1.0.12",
    description="Feature store recipe",
    author="Amit Boke",
    classifiers=["Programming Language :: Python :: 3.8"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["feast==0.34.1"],
    python_requires=">=3.8,<3.10",
    extras_require=extras_require,
)
