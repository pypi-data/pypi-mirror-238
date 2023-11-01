# graphpy_example_package

## Installation

You can use this Python package by following these steps:

### Step 1: Installation

#### From PyPI:

You can install the package from PyPI using pip:
https://pypi.org/project/graphpy-example-package/
```bash
pip install graphpy-example-package
```

#### From Local:

If you have the package locally, navigate to the root folder with `pyproject.toml` and run:

```bash
pip install ./
```

### Step 2: Import

You can import the package's modules as follows:

```python
from graphpy_example_package import gp_apis
```

### Testing

To run the package's test file located in the test folder, execute the following command:

```bash
python3 GCN_graphpy_test.py --gdir /mnt/huge_26TB/data/test2/cora/ --category 7 --graph binary
```

### Building the Python Package

To build the Python package, first install the necessary tools:

```bash
python3 -m pip install --upgrade build
```

Then build the package:

```bash
python3 -m build
```

### Uploading the Package to PyPI

To upload the package to PyPI, ensure you have the `twine` tool installed:

```bash
python3 -m pip install --upgrade twine
```

Then upload the package distribution:

```bash
python3 -m twine upload dist/*
```

## Instructions for Creating Python Packages

This is a sample project demonstrating how to create a Python library and publish it on PyPI. The structure and steps to create and distribute a Python package are outlined here.

### Reference Documentation

For detailed information on packaging and distributing Python projects, refer to the [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) tutorial on the official Python packaging website.

### Project Structure

Ensure your project follows the following structure:

```
graphpy_example_package/
├── LICENSE
├── pyproject.toml
├── README.md
├── src/
│   └── graphpy_example_package/
│       ├── __init__.py
│       └── gp_apis.py
└── tests/
```

1. The `src` directory contains your project's source code, and you should have an `__init__.py` file inside the `project_name` folder to mark it as a Python package.
2. Include a `LICENSE` file to specify the licensing terms of your project.
3. Write your project's README in Markdown format in the `README.md` file.
4. Place your project's tests in the `tests` directory.
5. The `pyproject.toml` file contains the project metadata and configuration.
6. All reference to local modules need to be import using package name: ex. `import kernel as gpk` need to be `from graphpy_example_package import kernel as gpk`

### pyproject.toml Configuration

Here's an example of a `pyproject.toml` configuration for your project:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "graphpy_example_package"
version = "0.0.1"
authors = [
  { name = "Your Name", email = "your@email.com" },
]
description = "A small example package"
readme = "README.md"
requires-python = ">=3.7"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

[project.urls]
homepage = "https://github.com/yourusername/graphpy_example_package"
bug-tracker = "https://github.com/yourusername/graphpy_example_package"
```

### Building and Distributing

To build and distribute your package, follow these steps:

1. Install the required tools:

```bash
sudo apt install python3-pip
pip3 install build
sudo apt install python3.10-venv
```

2. Build source distribution (sdist) and/or build distribution (wheel):

```bash
python3 -m build --sdist /path/to/your/project
python3 -m build --wheel /path/to/your/project
```

3. Install Twine for uploading:

```bash
sudo apt install twine
```

4. Upload your distribution files to PyPI:

```bash
twine upload dist/graphpy_example_package-0.0.1.tar.gz dist/graphpy_example_package-0.0.1-py3-none-any.whl
```

### API Token for PyPI Upload

If you encounter an API token issue during upload, create an API token on PyPI:

1. Username: `__token__`
2. Password: Your generated token
