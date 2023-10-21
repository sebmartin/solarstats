#!/bin/bash

if !which pip > /dev/null; then
    echo "Installing pip, this requires elevated privilegs and will prompt you for your password."
    sudo apt update && sudo apt install pip python3.11-venv sqlite3 -y
fi

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
        echo "Creating venv in $root_dir/.venv"
        python3 -m venv .venv
    fi

    echo "Activating venv"
    source .venv/bin/activate

    echo "Installing production requirements"
    pip install -r $root_dir/requirements.txt
    popd
}

create_venv