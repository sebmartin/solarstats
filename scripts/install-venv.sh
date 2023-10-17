#!/bin/bash

# Check if the script is run with superuser privileges (root)
if [ "$EUID" == 0 ]; then
    echo "Do not run this script with sudo."
    exit 1
fi

# Get the directory of the script
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the current working directory
root_dir=$(dirname $script_dir)

create_venv() {
    pushd $root_dir
    if [ ! -e "$file_path" ]; then
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install -r $root_dir/requirements.txt
    popd
}

create_venv