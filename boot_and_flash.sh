#!/bin/bash

# Execute DROPLET_BOOTLOADER.sh
sudo ./DROPLET_BOOTLOADER.sh

# Prompt the user to confirm before executing the flash
#read -p "Press Enter to proceed with the flash after bootloader..."
echo Flashing after bootloader...
# Execute DROPLET_FLASH.sh
sudo ./DROPLET_FLASH.sh

# Capture the output of pyserial-miniterm
output=$(sudo pyserial-miniterm /dev/ttyUSB0 38400)
echo $output
# Extract the Node ID using grep and awk
node_id=$(echo "$output" | grep "Node ID:" | awk '{print $3}')

# Extract the Version ID using grep and awk
version=$(echo "$output" | grep "Version:" | awk '{print $3}')

# Add the droplet info to the product database
python3 /home/testbench/droplets/Add_To_Database.py "$node_id" "$version"

# Pass the Node ID to Generate_Droplet_labels.py
python3 /home/testbench/droplets/Generate_Droplet_labels.py "$node_id"

wait 2
exit