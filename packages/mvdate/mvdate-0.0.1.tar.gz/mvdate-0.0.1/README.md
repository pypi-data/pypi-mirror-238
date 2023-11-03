[![PyPI version](https://badge.fury.io/py/mvdate.svg)](https://badge.fury.io/py/mvdate)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mvdate)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Code style: flake8](https://img.shields.io/badge/code%20style-flake8-456789.svg)](https://github.com/psf/flake8)
[![Downloads](https://static.pepy.tech/badge/mvdate)](https://pepy.tech/project/mvdate)
[![Downloads](https://static.pepy.tech/badge/mvdate/month)](https://pepy.tech/project/mvdate)
[![Downloads](https://static.pepy.tech/badge/mvdate/week)](https://pepy.tech/project/mvdate)
[![Donate](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/slackline/donate)

# mvdate

A Python package to search for files and move them to a directory structure based on date.

## Motivation

I keep my pictures in a hierarchical data structure of `YYYY/MM/DD` but that isn't how my camera stores them. I wanted
an easy way to copy/move files to this structure.

## Installation

In due course I will release to PyPI at which point it will be possible to...

``` bash
pip install mvdate
```

For now you need to clone and install.

``` bash
git clone git@gitlab.com:nshephard/mvdate.git
cd mvdate
pip install .
```

Or you can use `pip` to install directly

``` bash
pip install mvdate@git+https://gitlab.com/nshephard/mvdate.git@main
```

## Usage

To search the current directory for files ending with `png` and move them to `~/pics/YYYY/MM/DD/`

``` bash
mvdate --base ./ --destination ~/pics/ --ext png
```

For all options see the help

``` bash
mvdate --help
```

## Links
