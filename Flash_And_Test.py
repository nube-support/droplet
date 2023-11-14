import subprocess
import Custom_Logger, logging, Manufacturing_Info, Add_To_Database_Print_Labels
import sys
from termcolor import *

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
    subprocess.run(["sudo", "./DROPLET_BOOTLOADER.sh"])

    # Prompt the user to confirm before executing the flash
    # input("Press Enter to proceed with the flash after bootloader...")
    print("Flashing after bootloader...")

    # Execute DROPLET_FLASH.sh
    subprocess.run(["sudo", "./DROPLET_FLASH.sh"])

    Add_To_Database_Print_Labels.main(technician, hardware_version, batch_id, manufacturing_order, print_flag)
    
    # Run the reset command using a shell
    subprocess.run('reset', shell=True)

    with open('cleaned_output.txt', "r") as file:
        for line in file:
            print(line.strip())

    input(colored('Insert new device, press reset button and press enter to execute script. Press Ctrl+c to stop.\n', 'white', 'on_blue'))

