from setuptools import setup, find_packages

import os
print(os.curdir)

setup(
    name="pyreportgen",
    version="0.1.1",
    description="A package for creating reports and other pdf documents.",
    long_description=
"""
# Pyreportgen
This is a pyton library for creating reports and other content in the form of a pdf using python.


## Requirements.
- `wkhtmltopdf`

## Example 
```py
import pyreportgen as rg 
import pyreportgen.layout as layout

report = rg.Report([
    rg.Header("Hello World"),
    rg.Text("This is a sample of how to use pyreportgen"),
    Layout.HBox([
        rg.Text("This is a paragraph in a box."),
        rg.Text("These will be placed next to each other"),
        rg.Text("All the boxes will have equal space regardless of content.")
    ])
])

report.pdf("out.pdf")
```
""",
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)