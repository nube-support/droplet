import subprocess
import helpers.Custom_Logger as Custom_Logger, helpers.Manufacturing_Info as Manufacturing_Info, Droplet_Test_Process
import sys, json, os
from termcolor import *
from productsdb import products

with open('configs/TH_prod.json', 'r') as config_file:
    config = json.load(config_file)

products.init_db_path(config["db_path"])
local_test_path = config["local_test_path"]
variant = config["variant"]
make = config["make"]
model = config["model"]

# Get the directory of the current script and parent
script_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(script_directory)

# Check if argument not to print has been passed in the terminal
print_flag = ''
if len(sys.argv) > 1 and print_flag == '':
    if sys.argv[1] == '--no-print':
        print_flag = sys.argv[1]

technician, hardware_version, batch_id, manufacturing_order = None, None, None, None
Custom_Logger.create_logger('output.txt')  # Set up the custom logging configuration

while True:
    #make sure the test output file is clean for each device
    with open('output.txt', "w") as file:
        file.truncate(0)  

    # Check if technician and info is still the same
    if None not in (technician, hardware_version, batch_id, manufacturing_order):
        technician, hardware_version, batch_id, manufacturing_order = Manufacturing_Info.current_technician_and_info(technician, hardware_version, batch_id, manufacturing_order)
    else:
        # First execution of script, get technician and info
        technician, hardware_version, batch_id, manufacturing_order = Manufacturing_Info.current_technician_and_info()
        input(colored('Press the reset button on the device and press enter to execute the script.\n', 'white', 'on_blue'))

    # Execute DROPLET_BOOTLOADER.sh
    # subprocess.run(["sudo", "./DROPLET_BOOTLOADER.sh"])
    #subprocess.run(["sudo", f".{os.path.join(parent_directory, 'droplet', 'helpers', 'scripts', 'DROPLET_BOOTLOADER.sh')}"])
    #subprocess.run(["sudo", "/home/testbench/helpers/scripts/DROPLET_BOOTLOADER.sh"])
    subprocess.run(["sudo", "./DROPLET_BOOTLOADER.sh"])
    print("Flashing after bootloader...")

    # Execute DROPLET_FLASH.sh
    #subprocess.run(["sudo", f".{os.path.join(parent_directory, 'droplet', 'helpers', 'scripts', 'DROPLET_FLASH.sh')}"])
    subprocess.run(["sudo", "./DROPLET_FLASH.sh"])
    Droplet_Test_Process.main(technician, make, model, variant, hardware_version, batch_id, manufacturing_order, print_flag, local_test_path)
    # Run the reset command using a shell
    subprocess.run('reset', shell=True)
    failed_flag = False
    with open('cleaned_output.txt', "r") as file:
        for line in file:
            if 'Failed' in line:
                failed_flag = True
                print(colored(line, 'white', 'on_red'))
                input(colored('Test Failed, check reason above. Press Ctrl+c to stop, or press reset button and enter to retry.\n', 'white', 'on_blue'))
            elif 'Working' in line:
                print(colored(line, 'white', 'on_green'))

            else:
                print(line.strip())
    
    if failed_flag:
        continue
    else:
        if print_flag != '--no-print':
            cmd = 'lpr -P PT-P900W -o PageSize=Custom.12x48mm -o Resolution=360dpi -o CutLabel=0 -o ExtraMargin=0mm -o number-up=1 -o orientation-requested=4 -#2 /home/testbench/droplet/images/product_label.png'
            subprocess.check_output(cmd, shell=True, text=True)

    input(colored('Insert new device, press reset button and press enter to execute script. Press Ctrl+c to stop.\n', 'white', 'on_blue'))

