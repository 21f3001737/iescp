#!/bin/bash

DIRECTORY=$(dirname "$0")

if [ ! -d "$DIRECTORY/venv" ]; then
  python -m venv $DIRECTORY/venv
fi

source $DIRECTORY/venv/bin/activate
pip install --upgrade pip

pip install -r $DIRECTORY/requirements.txt 

python $DIRECTORY/main.py

