# pyprocessors_restore_punctuation

[![license](https://img.shields.io/github/license/oterrier/pyprocessors_restore_punctuation)](https://github.com/oterrier/pyprocessors_restore_punctuation/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyprocessors_restore_punctuation/workflows/tests/badge.svg)](https://github.com/oterrier/pyprocessors_restore_punctuation/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyprocessors_restore_punctuation)](https://codecov.io/gh/oterrier/pyprocessors_restore_punctuation)
[![docs](https://img.shields.io/readthedocs/pyprocessors_restore_punctuation)](https://pyprocessors_restore_punctuation.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyprocessors_restore_punctuation)](https://pypi.org/project/pyprocessors_restore_punctuation/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyprocessors_restore_punctuation)](https://pypi.org/project/pyprocessors_restore_punctuation/)

Create segments from annotations

## Installation

You can simply `pip install pyprocessors_restore_punctuation`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyprocessors_restore_punctuation
```

### Running the test suite

You can run the full test suite against all supported versions of Python (3.8) with:

```
tox
```

### Building the documentation

You can build the HTML documentation with:

```
tox -e docs
```

The built documentation is available at `docs/_build/index.html.
