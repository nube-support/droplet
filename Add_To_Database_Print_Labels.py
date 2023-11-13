from datetime import datetime
import subprocess, products
import re, logging, Custom_Logger, shutil, os, sys, Generate_Droplet_labels
from termcolor import *

Custom_Logger.create_logger('output.txt')  # Set up the custom logging configuration
local_test_path = f"/home/testbench/product_database/"
print_flag = ''

def get_info():
    if len(sys.argv) >= 5:
        technician = sys.argv[1]
        hardware_version = sys.argv[2]
        batch_id = sys.argv[3]
        manufacturing_order = sys.argv[4]
    return technician, hardware_version, batch_id, manufacturing_order
    
def main():
    technician, hardware_version, batch_id, manufacturing_order = get_info()

    # if len(sys.argv == 6):
    #     print_flag = sys.argv[6]

    product_in_db = ''

    try:
        command = "sudo pyserial-miniterm /dev/ttyUSB0 38400"

        # Set a timeout (e.g., 2 seconds)
        timeout = 2

        with open('output.txt', 'a') as output_file:
            result = subprocess.run(
                command, shell=True, stdout=output_file, stderr=subprocess.PIPE, text=True, timeout=timeout
            )
            logging.info(result)

        if result.returncode == 0:
            # Command succeeded
            print("Command succeeded.")
        else:
            # Command failed
            print("Command failed. Error:")
            print(result.stderr)

    except subprocess.TimeoutExpired:
        # Handle a timeout here
        print("Succesfully retrieved test information")

    output_file = "cleaned_output.txt"

    for _ in range(20):
        command = 'sudo ./clean_script.sh'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Print a message indicating that the cleaning process is complete
    print("Content cleaned and saved to", output_file)

    with open("cleaned_output.txt", "r") as file:
        output = file.read()

    # Define the regular expressions for Node ID and Version
    node_id_pattern = r"Node ID:\s*(\w+)"
    version_pattern = r"^\s*Version:\s*([\d.]+)\s*$"
    dip_switches_pattern = r"dip_(\d+)\s*:\s*(\d+)"

    # Iterate over lines
    for line in output.splitlines():
        # Check if the line contains the version information
        version_match = re.match(r"^\s*Version:\s*([\d.]+)\s*$", line)
        if version_match:
            software_version = version_match.group(1).strip()
            continue

    # Extract the Node ID using regular expressions
    node_id_match = re.search(node_id_pattern, output)
    node_id = node_id_match.group(1) if node_id_match else ""

    # Extract the Dip Switches using regular expressions
    # dip_switch_matches = re.findall(dip_switches_pattern, output)
    # dip_switch_states = {f"dip_{number}": state for number, state in dip_switch_matches}

    # Check if all dip switches are 0 except dip switch 5
    # if dip_switch_states.get("dip_5") == "1" and all(state == "0" for number, state in dip_switch_states.items() if number != "dip_5"):
    #     logging.info(colored("All dip switches are 0 except dip switch 5.", 'white', 'on_green'))
    # else:
    #     logging.info(colored("Dip switches are not in the expected state.", 'white', 'on_green'))
    
    comments = "None"

    if node_id != '':
        print(node_id)
        #Check if product was tested before and update it in that case
        product_in_db = products.get_product_by_serial_number(node_id)

    if product_in_db is not None:
        barcode = products.update_product_via_serial(manufacturing_order, 'DL', 'TH', node_id, hardware_version, batch_id, software_version, technician, True, "Tested more than once")
    else:
        barcode = products.add_product(manufacturing_order, 'DL', 'TH', node_id, hardware_version, batch_id, software_version, technician, True, comments)

    # Pass the Node ID to Generate_Droplet_labels.py
    #subprocess.run(["sudo python3", "/home/testbench/droplets/Generate_Droplet_labels.py"])
    Generate_Droplet_labels.main(barcode, hardware_version, software_version)

    # Copy the contents of the old file to the new file
    shutil.copyfile('cleaned_output.txt', f"{local_test_path}{barcode}.txt")
    return barcode
if __name__ == '__main__':
    main()
    #cmd = 'lpr -P PT-P900W -o PageSize=Custom.12x48mm -o Resolution=360dpi -o CutLabel=0 -o ExtraMargin=0mm -o number-up=1 -o orientation-requested=4 -#2 product_label.png'
    #subprocess.check_output(cmd, shell=True, text=True)

    #barcode = products.update_product_via_serial('mo00025', 'A1B2C6AD', '0.62', '2331', '2.3', 'Kakn', True, "testah")
   # barcode = products.add_product('mo00025', 'DL', 'TH', 'A1B2C6AD', '0.62', '2331', '2.3', 'Kakn', True, "testah")
