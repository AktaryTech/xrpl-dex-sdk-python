#!/bin/bash

poetry run pytest

if [ $1 == "ws" ]; then
    ./.venv/bin/python3 tests/watch_methods.py
fi
