#!/usr/bin/env bash

CONFOID_CWD=$(pwd)
CONFOID_VENV_PATH="$CONFOID_CWD/.venv"

if [[ ! -f "$CONFOID_VENV_PATH/bin/activate" ]]; then
    python3 -m venv $CONFOID_VENV_PATH
    source $CONFOID_VENV_PATH/bin/activate
    pip install pip --upgrade
    pip install -e ".[dev]"
else
    source $CONFOID_VENV_PATH/bin/activate
fi

cd $CONFOID_CWD

rm -rf dist/*
python3 setup.py sdist
twine upload --verbose dist/*
