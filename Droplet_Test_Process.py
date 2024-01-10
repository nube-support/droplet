from datetime import datetime
import subprocess
from productsdb import products
import re, logging, helpers.Custom_Logger as Custom_Logger, shutil, os, sys, labels.Generate_Droplet_labels as Generate_Droplet_labels
from termcolor import *

Custom_Logger.create_logger('output.txt')  # Set up the custom logging configuration
print_flag = ''
  
def main(technician, make, model, variant, hardware_version, batch_id, manufacturing_order, print_flag, local_test_path):
    comments = "None"

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
    output = ''
    for _ in range(20):
        command = 'sudo ./clean_script.sh'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Print a message indicating that the cleaning process is complete
    print("Content cleaned and saved to", output_file)

    with open("cleaned_output.txt", "r") as file:
        output = file.read()

    # Define the regular expressions for Node ID and Version
    node_id_pattern = r"Node ID:\s*(\w+)"
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
    dip_switch_matches = re.findall(dip_switches_pattern, output)
    dip_switch_states = {f"dip_{number}": state for number, state in dip_switch_matches}

    # Check if all dip switches are 0 except dip switch 5
    if dip_switch_states.get("dip_5") == "1" and all(state == "0" for number, state in dip_switch_states.items() if number != "dip_5"):
        with open("cleaned_output.txt", "a") as output_file:
            output_file.write("Working - All dip switches are 0 except dip switch 5.\n")
            comments += 'Dipswitch'
    else:
        with open("cleaned_output.txt", "a") as output_file:
            output_file.write("Failed - Dip switches are not in the expected state.\n")

    if node_id != '':
        #Check if product was tested before and update it in that case
        product_in_db = products.get_products_by_loraid(node_id)

    if product_in_db is not None:
        barcode = products.update_product(manufacturing_order, f"{make}-{model}-{node_id}", 'No-serial', hardware_version, batch_id, 
                                          software_version, technician, True, comments)
    else:
        barcode = products.add_product(manufacturing_order, make, model, variant, node_id, 'No-serial', 
                                       hardware_version, batch_id, software_version, technician, True, comments)

    # Generate labels
    Generate_Droplet_labels.main(make, model, variant, barcode, hardware_version, software_version, print_flag)

    # Copy the contents of the old file to the new file
    shutil.copyfile('cleaned_output.txt', f"{local_test_path}{barcode}.txt")
    return barcode

if __name__ == '__main__':
    main()
