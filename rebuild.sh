#!/bin/bash

PACKAGE_NAME=django-cache-toolbox-modified
rm -rf dist $PACKAGE_NAME.egg-info
python setup.py sdist upload
pip uninstall $PACKAGE_NAME
rm -rf ~/.virtualenvs/package-dev/build/$PACKAGE_NAME
pip install $PACKAGE_NAME
