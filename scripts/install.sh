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

function install_venv() {

    if ! which pip > /dev/null; then
        echo "Installing pip, this requires elevated privilegs and will prompt you for your password."
        sudo apt update && sudo apt install pip python3.11-venv sqlite3 -y
    fi

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

install_systemd_service() {
    # Set the service name and description
    service_name="solarstats"

    # Define the path to your systemd service template relative to the script's directory
    template_file="$script_dir/systemd/solarstats.service.template"

    # Check if the template file exists
    if [ ! -f "$template_file" ]; then
        echo "Service template file not found: $template_file"
        exit 1
    fi

    # Create a systemd unit file from the template
    mkdir -p "$root_dir/systemd/"
    output_file="$root_dir/systemd/$service_name.service"
    sed -e "s|{{INSTALL_PATH}}|$root_dir|g" "$template_file" > "$output_file"

    echo Installation complete.
    echo
    echo To install as a system service and have it run when the system boots up, run
    echo the following commands:
    echo
    echo "  sudo cp $output_file /etc/systemd/system/"
    echo "  sudo systemctl daemon-reload"
    echo "  sudo systemctl enable \"$service_name\""
    echo "  sudo systemctl start \"$service_name\""
}

! [ -e "$root_dir/.venv" ] && install_venv

# (systemctl list-units --type=service | awk '$1 == "solarstats.service" { print $1 }') ||
install_systemd_service
