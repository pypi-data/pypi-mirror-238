from setuptools import setup, find_packages

import os
readme = open("./readme.md").read()

print(os.listdir())
print(find_packages("./pyreportgen/", include="__init__.py"))

setup(
    name="pyreportgen",
    version="0.1.2",
    description="A package for creating reports and other pdf documents.",
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)