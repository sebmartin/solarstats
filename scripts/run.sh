#!/bin/bash

# Get the directory of the script
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
root_dir=$(dirname $script_dir)

pushd $root_dir
source .venv/bin/activate
python -m solarstats $@
popd