#!/bin/bash

CURRENT_DIR="$(dirname -- "$BASH_SOURCE")"
echo $CURRENT_DIR

pip install -r "$CURRENT_DIR/../requirements.txt"

pytest "$CURRENT_DIR/../data/pipelinetests.py"
