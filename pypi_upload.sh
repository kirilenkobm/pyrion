#!/usr/bin/env bash
rm -rf dist/
python -m build --sdist --wheel
python -m twine upload dist/*
