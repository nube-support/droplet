import subprocess
import time
import sys

# Check if argument not to print has been passed in the terminal
print_flag = ''
if len(sys.argv) > 1 and print_flag == '':
    if sys.argv[1] == '--no-print':
        print_flag = sys.argv[1]

# Execute DROPLET_BOOTLOADER.sh
subprocess.run(["sudo", "./DROPLET_BOOTLOADER.sh"])

# Prompt the user to confirm before executing the flash
# input("Press Enter to proceed with the flash after bootloader...")
print("Flashing after bootloader...")

# Execute DROPLET_FLASH.sh
subprocess.run(["sudo", "./DROPLET_FLASH.sh"])

# Execute pyserial-miniterm and capture its output
try:
    result = subprocess.run(["sudo", "pyserial-miniterm", "/dev/ttyUSB0", "38400"], text=True, capture_output=True, check=True)
    output = result.stdout
except subprocess.CalledProcessError as e:
    print(f"Error executing pyserial-miniterm: {e}")
    output = ""

# Extract the Node ID using regular expressions
import re
node_id_match = re.search(r"Node ID:\s*(\w+)", output)
node_id = node_id_match.group(1) if node_id_match else ""

# Extract the Version ID using regular expressions
version_match = re.search(r"Version:\s*(\w+)", output)
version = version_match.group(1) if version_match else ""

print(node_id)
print(version)
# Add the droplet info to the product database
#subprocess.run(["python3", "/home/testbench/droplets/Add_To_Database.py", node_id, version])

if print_flag != '':
    # Pass the Node ID to Generate_Droplet_labels.py
    subprocess.run(["python3", "/home/testbench/droplets/Generate_Droplet_labels.py", node_id])

# Wait for a few seconds
time.sleep(2)

