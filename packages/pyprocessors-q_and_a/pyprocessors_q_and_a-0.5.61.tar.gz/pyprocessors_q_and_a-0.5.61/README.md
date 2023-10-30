# pyprocessors_q_and_a

[![license](https://img.shields.io/github/license/oterrier/pyprocessors_q_and_a)](https://github.com/oterrier/pyprocessors_q_and_a/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyprocessors_q_and_a/workflows/tests/badge.svg)](https://github.com/oterrier/pyprocessors_q_and_a/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyprocessors_q_and_a)](https://codecov.io/gh/oterrier/pyprocessors_q_and_a)
[![docs](https://img.shields.io/readthedocs/pyprocessors_q_and_a)](https://pyprocessors_q_and_a.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyprocessors_q_and_a)](https://pypi.org/project/pyprocessors_q_and_a/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyprocessors_q_and_a)](https://pypi.org/project/pyprocessors_q_and_a/)

Processor based on Facebook's q_and_a

## Installation

You can simply `pip install pyprocessors_q_and_a`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyprocessors_q_and_a
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
