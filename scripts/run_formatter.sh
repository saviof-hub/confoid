#!/usr/bin/env bash

isort src/confoid/

black src/confoid/

flake8 src/confoid/

bandit -v -r src/confoid/

# pylint src/confoid/

# mypy src/confoid/
