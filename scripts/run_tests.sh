#!/usr/bin/env bash

CONFOID_CWD=${PWD}
CONFOID_VENV_PATH="$CONFOID_CWD/.venv"

if [[ ! -f "$CONFOID_VENV_PATH/bin/activate" ]]; then
    python3 -m venv $CONFOID_VENV_PATH
    source $CONFOID_VENV_PATH/bin/activate
    pip install pip --upgrade
    pip install -e ".[dev]"
fi

cd $CONFOID_CWD
source $CONFOID_VENV_PATH/bin/activate

pytest
