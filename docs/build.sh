#!/bin/bash

poetry run sphinx-apidoc -f -o . ../xrpl_dex_sdk && make html
