#!/bin/bash

# Check if the script is run with superuser privileges (root)
if [ "$EUID" -ne 0 ]; then
    echo "This script requires superuser privileges. Please run it with sudo."
    exit 1
fi

# Get the directory of the script
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the current working directory
root_dir=$(dirname $script_dir)

create_systemd_service() {

    # Set the service name and description
    service_name="solarstats"

    # Define the path to your systemd service template relative to the script's directory
    template_file="$script_dir/systemd/solarstats.service"

    # Check if the template file exists
    if [ ! -f "$template_file" ]; then
        echo "Service template file not found: $template_file"
        exit 1
    fi

    # Define the path to the output service file
    # output_file="/etc/systemd/system/$service_name.service"
    output_file="$root_dir/systemd/$service_name.service"
    mkdir -p "$root_dir/systemd/"

    # Replace the executable path in the template with the current working directory
    sed -e "s|{{INSTALL_PATH}}|$root_dir|g" "$template_file" > "$output_file"

    # Reload systemd to pick up the new service file
    systemctl daemon-reload

    # # Enable and start the service
    systemctl enable "$service_name"
    systemctl start "$service_name"
}

create_systemd_service