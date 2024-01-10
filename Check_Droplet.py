import subprocess
import re, logging
from termcolor import *

def main():
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
    dip_switches_pattern = r"dip_(\d+)\s*:\s*(\d+)"
    
    # Extract the Dip Switches using regular expressions
    dip_switch_matches = re.findall(dip_switches_pattern, output)
    dip_switch_states = {f"dip_{number}": state for number, state in dip_switch_matches}

    # Check if all dip switches are 0 except dip switch 5
    if dip_switch_states.get("dip_5") == "1" and all(state == "0" for number, state in dip_switch_states.items() if number != "dip_5"):
        with open("cleaned_output.txt", "a") as output_file:
            output_file.write("Working - All dip switches are 0 except dip switch 5.\n")
    else:
        with open("cleaned_output.txt", "a") as output_file:
            output_file.write("Failed - Dip switches are not in the expected state.\n")

    # Run the reset command using a shell
    subprocess.run('reset', shell=True)

    with open('cleaned_output.txt', "r") as file:
        for line in file:
            print(line.strip())

if __name__ == '__main__':
    main()
