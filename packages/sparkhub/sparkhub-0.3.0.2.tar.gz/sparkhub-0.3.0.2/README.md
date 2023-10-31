# sparkhub

## Overview

sparkhub is a Python package that provides a set of utilities for running spark pipelines on Google Cloud Platform (GCP) and in an on-prem cluster. It includes functions for generating Hail headers, running Hail pipelines on Dataproc clusters, and managing GCP resources.

## Main Features

- Generate Hail headers for use in Hail pipelines
- Run Hail pipelines on Dataproc clusters
- Manage GCP resources, such as Dataproc clusters and Google Cloud Storage buckets

## Installation

To install sparkhub, you can use pip:

`pip install sparkhub`

## vscode settings

Before running sparkhub from vscode, you must change your user settings. Make sure the `Jupyter > Interactive Window > Text Editor: Magic Commands As Comments` option is checked. This will allow you to use magic commands in the interactive window of vscode.

To change your user settings, open the command palette in vscode (using the `Ctrl+Shift+P` keyboard shortcut) and search for "Preferences: Open User Settings".

## Usage

To use sparkhub, you can import the relevant functions into your Python code:

```python
from sparkhub.hailrunner import get_hail_header, HailRunnerGC, RunnerMagics
from sparkhub.submit import *
```

Then, you can call the functions with the appropriate arguments to generate headers, run pipelines, and manage GCP resources.

## Maintainer

sparkhub is maintained by TJ Singh. If you have any questions or issues, please contact him at <ts3475@cumc.columbia.edu>.
