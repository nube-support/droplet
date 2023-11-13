import argparse
import sqlite3
from datetime import datetime
import os
db_path = '/home/testbench/product_database/products.db'  # Specify the full path to the database

def get_product_by_serial_number(serial_number):
    global db_path
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Query the database to find the product with the specified serial number
    c.execute('''
        SELECT * FROM products
        WHERE SerialNumber = ?
    ''', (serial_number,))

    product = c.fetchone()
    conn.close()

    return product

def get_next_serial(cursor):
    cursor.execute("SELECT BarCodeID FROM products ORDER BY BarCodeID DESC LIMIT 1")
    row = cursor.fetchone()
    if row:
        serial = row[0] + 1
        if serial >= 4294967295:
            serial = 359956882
    else:
        serial = 359956882  # Set initial SerialID to 2024 if no records found
    return serial


def database_exists():
    global db_path
    return os.path.exists(db_path)


def create_db():
    global db_path
    if not database_exists():
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE products (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ManufacturingOrder TEXT,
            Make TEXT,
            Model TEXT,
            BarCodeID INTEGER,
            TestingDateCode TEXT,
            SerialNumber TEXT,
            HardwareVersion TEXT,
            HardwareBatch TEXT,
            SoftwareVersion TEXT,
            Technician TEXT,
            TestDate TEXT,
            PassedAllTests BOOLEAN,
            Comments LONGTEXT
        )''')
        conn.commit()
        conn.close()


def add_product(manufacturing_order, make, model, bar_code_id, testing_date_code, serial_number, hardware_version, hardware_batch,
                software_version, technician, test_date, passed_all_tests, comments):
    global db_path
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''
        INSERT INTO products (
            ManufacturingOrder,
            Make,
            Model,
            BarCodeID,
            TestingDateCode,
            SerialNumber,
            HardwareVersion,
            HardwareBatch,
            SoftwareVersion,
            Technician,
            TestDate,
            PassedAllTests,
            Comments
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (manufacturing_order, make, model, bar_code_id, testing_date_code, serial_number, hardware_version, hardware_batch,
          software_version, technician, test_date, passed_all_tests, comments))

    conn.commit()
    conn.close()


def add_product(manufacturing_order, make, model, serial_number, hardware_version, hardware_batch,
                software_version, technician, passed_all_tests, comments):
    global db_path
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    bar_code_id = get_next_serial(c)
    current_date = datetime.now()
    testing_date_code = hardware_batch
    bar_code_id_hex = format(bar_code_id, '08X')  # Convert serial_id to 4-digit hexadecimal
    barcode_number = f'{make}-{model}-{bar_code_id_hex}'
        
    #barcode_number = f'{make}-{model}-{serial_number}'
    test_date = current_date.strftime('%Y-%m-%d %H:%M:%S')
    c.execute('''
         INSERT INTO products (
             ManufacturingOrder,
             Make,
             Model,
             BarCodeID,
             TestingDateCode,
             SerialNumber,
             HardwareVersion,
             HardwareBatch,
             SoftwareVersion,
             Technician,
             TestDate,
             PassedAllTests,
             Comments
         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
     ''', (manufacturing_order, make, model, bar_code_id, testing_date_code, serial_number, hardware_version, hardware_batch,
           software_version, technician, test_date, passed_all_tests, comments))

    conn.commit()
    conn.close()
    return barcode_number

def update_product(barcode, new_serial_number, new_hardware_version, new_hardware_batch, new_software_version, new_technician, new_passed_all_tests, new_comments):
    global db_path

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Split the barcode and extract the necessary fields to identify the record
    make, model, serial_id_hex = barcode.split('-')
    serial_id = int(serial_id_hex, 16)

    # Update the product in the database
    c.execute('''
        UPDATE products
        SET SerialNumber = ?,
            HardwareVersion = ?,
            HardwareBatch = ?,
            SoftwareVersion = ?,
            Technician = ?,
            PassedAllTests = ?,
            Comments = ?
        WHERE Make = ? AND Model = ? AND BarCodeID = ?
    ''', (new_serial_number, new_hardware_version, new_hardware_batch, new_software_version, new_technician, new_passed_all_tests, new_comments, make, model, serial_id))


    conn.commit()
    conn.close()
    return barcode

def update_product_via_serial(new_manufacturing_order, make, model, serial_number, new_hardware_version, new_hardware_batch, new_software_version, new_technician, new_passed_all_tests, new_comments):
    global db_path

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Update the product in the database
    c.execute('''
        UPDATE products
        SET ManufacturingOrder = ?,
            HardwareVersion = ?,
            HardwareBatch = ?,
            SoftwareVersion = ?,
            Technician = ?,
            PassedAllTests = ?,
            Comments = ?
        WHERE SerialNumber = ?
    ''', (new_manufacturing_order, new_hardware_version, new_hardware_batch, new_software_version, new_technician, new_passed_all_tests, new_comments, serial_number))


    # Retrieve the updated barcode
    c.execute('SELECT BarCodeID FROM products WHERE SerialNumber = ?', (serial_number,))
    barcode_tuple = c.fetchone()
    
    conn.commit()
    conn.close()
    bar_code_id_hex = format(barcode_tuple[0], '08X')
    barcode_number = f'{make}-{model}-{bar_code_id_hex}'

    # Return the barcode as a string
    return barcode_number if barcode_tuple else None

def get_products(date_code):
    global db_path
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Query the database to find products with the specified TestingDateCode
    c.execute('''
        SELECT * FROM products
        WHERE TestingDateCode = ?
    ''', (date_code,))

    products = c.fetchall()
    conn.close()

    return products


def get_product(barcode):
    global db_path
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Split the barcode and extract the necessary fields to identify the record
    make, serial_id_hex, testing_date_code = barcode.split('-')
    serial_id = int(serial_id_hex, 16)  # Convert hex to int for serial_id

    # Query the database to find the product
    c.execute('''
        SELECT * FROM products
        WHERE Make = ? BarCodeID = ? AND TestingDateCode = ?
    ''', (make, serial_id, testing_date_code))

    product = c.fetchone()
    conn.close()

    return product


# Usage:
create_db()
# Example usage of the add_product function
if __name__ == "__main__":
    # manufacturing_order = 'M00025'
    # make = "RC"
    # model = '0006'
    # serial_number = "SN123456"
    # hardware_version = "1.2"
    # hardware_batch = "2341"
    # software_version = "SW1.0.1"
    # technician = "John Doe"
    # passed_all_tests = True
    # comments = "All tests passed. Ready for shipping."

    # Call the add_product function
    # barcode = add_product(manufacturing_order, make, model, serial_number, hardware_version, hardware_batch,
    #             software_version, technician, passed_all_tests, comments)
    #create_db()

    a = get_product_by_serial_number('A1B2C6AD')
    if a:
        print(a)
    #barcode = update_product_via_serial('mo00025', 'DL', 'TH', 'A1B2C6AD', '0.62', '2331', '2.3', 'Name', True, "test")
    barcode = add_product('mo00025', 'DL', 'TH', 'A1B2C6AD', '0.62', '2331', '2.3', 'Kakn', True, "testah")
    print(barcode)
# update_product(barcode, 'CSN456', '00:AA:BB:CC:DD:EE', '11:22:33:44:55:66', True, 'All tests passed successfully')/
# print(barcode)
# product = get_product(barcode)
# if product:
#     print(product)
# else:
#     print(f"No product found for barcode: {barcode}")
# products = get_products('2344')
# for product in products:
#     print(product)


