## README - Droplet Manufacturing

Documentation for Flashing and Testing Droplets:

https://docs.google.com/document/d/16Bl6WByoPQxH0keD4DW0MGktjZCH5ZyhydPQtKvMK4g/edit#heading=h.jci4fax0p0nk

### Prerequisites

1. **Install needed packages**: Required to add and update products in the database. You can install it with:

Make sure to install all dependencies by running the command below:

```bash
pip install -r requirements.txt
```

Current packages include:
productsdb: A library for adding/updating/deleting products and retrieving valuable information.
2. **Choose a testing configuration**:

Depending on the make and model of the product you are manufacturing, check the config folder for the correct one and change the initial lines of the script that loads this info.

If you are a developer make sure to use the test configs in order to not polute the production database.

### Running the scripts

To flash and test a device:

```bash
sudo python3 Flash_and_Test.py
```

To check the health of a finished product:

```bash
sudo Check_Droplet.py
```

Make sure you are in the script's directory.

### Notes

- The script may request user input to continue during some checks.
- Ensure to use sudo when executing tests.
- Refer to the pdf documentation for in-depth test execution examples.

**Disclaimer**: This script is intended for diagnostic purposes and may need further customization or additional checks based on your specific requirements as development unfolds.