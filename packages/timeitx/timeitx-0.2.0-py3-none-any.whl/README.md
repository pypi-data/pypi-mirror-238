# timeitX - Function Execution Time Logger

<p align="center">
<a href="https://github.com/aws-samples/eks-cluster-upgrade/actions/workflows/validate.yaml"><img alt="Validation Status" src="https://github.com/aws-samples/eks-cluster-upgrade/actions/workflows/validate.yaml/badge.svg?branch=main&event=push"></a>
<a href="https://github.com/aws-samples/eks-cluster-upgrade/actions/workflows/e2e-test.yaml"><img alt="E2E Cluster Upgrade" src="https://github.com/aws-samples/eks-cluster-upgrade/actions/workflows/e2e-test.yaml/badge.svg?branch=main"></a>
<a href="https://codecov.io/github/aws-samples/eks-cluster-upgrade?branch=main"><img alt="Coverage Status" src="https://codecov.io/github/aws-samples/eks-cluster-upgrade/coverage.svg?branch=main"></a>
<a href="https://pypi.org/project/eksupgrade/"><img alt="PyPI" src="https://img.shields.io/pypi/v/eksupgrade"></a>
<a href="https://pepy.tech/project/eksupgrade"><img alt="Downloads" src="https://pepy.tech/badge/eksupgrade"></a>
</p>


![GitHub](https://img.shields.io/github/license/nitishsaik/timeitX)
![GitHub](https://img.shields.io/github/issues/nitishsaik/timeitX)
![GitHub](https://img.shields.io/github/stars/nitishsaik/timeitX)

`timeitX` is a Python decorator that logs the execution time of functions, both for synchronous and asynchronous functions.

## Features

- Log the execution time of functions.
- Supports both synchronous and asynchronous functions.
- Customizable function names for logging.
- Precision down to milliseconds.
- Easy to integrate with your Python projects.

## Installation

You can install `timeitX` via pip:

```bash
pip install timeitX
```

## Usage

```python

from timeitX import timeitX

# Define your logger
import logging
logger = logging.getLogger("timeitX")

@timeitX(name="My Function", logger=logger)
def my_function():
    # Your function code here

# For asynchronous functions
@timeitX(name="Async Function", logger=logger)
async def async_function():
    # Your async function code here

```
