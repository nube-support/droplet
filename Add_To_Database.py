from datetime import datetime
import subprocess, sys, products


def main():

    droplet_id = sys.argv[1].strip()
    version = sys.argv[2].strip()

    if droplet_id != '':
        barcode = products.update_product(barcode, System_Info.serial_number(ssh_client), hardware_version, batch_id,
                    version, technician, True, comments)

        barcode = products.add_product(manufacturing_order, 'DR', 'B2', System_Info.serial_number(ssh_client), hardware_version, batch_id,
                        rc_version, technician, True, comments)

if __name__ == '__main__':
    main()
    cmd = 'lpr -P PT-P900W -o PageSize=Custom.12x48mm -o Resolution=360dpi -o CutLabel=0 -o ExtraMargin=0mm -o number-up=1 -o orientation-requested=4 -#2 product_label.png'
    subprocess.check_output(cmd, shell=True, text=True)
