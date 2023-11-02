| PyPI Release | Test Status | Code Coverage |
| ------------ | ----------- | ------------- |
| [![PyPI version](https://badge.fury.io/py/rms-interval.svg)](https://badge.fury.io/py/rms-interval) | [![Build status](https://img.shields.io/github/actions/workflow/status/SETI/rms-interval/run-tests.yml?branch=master)](https://github.com/SETI/rms-interval/actions) | [![Code coverage](https://img.shields.io/codecov/c/github/SETI/rms-interval/main?logo=codecov)](https://codecov.io/gh/SETI/rms-interval) |

# rms-interval

PDS Ring-Moon Systems Node, SETI Institute

Supported versions: Python >= 3.7

The interval class behaves like a dictionary keyed by ranges of
floating-point numbers. Each value of the dictionary applies for any key
value within the numeric range. Later entries into the dictionary can
partially or completely replace earlier values.

Note that this package is deprecated in favor of the `portion` module.
Eventually this package may be removed entirely.
