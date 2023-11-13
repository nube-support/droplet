#!/bin/bash

port_number=0
port_found=false
serial_port=""

while [ "$port_found" = false ]; do
    serial_port="/dev/ttyUSB${port_number}"

    if [ -e "$serial_port" ]; then
        echo "Serial port found: $serial_port"
        port_found=true
    else
        echo "Serial port $serial_port not found. Trying the next port..."
        ((port_number++))
    fi
done

yeet() {

    #/home/nube/.arduino15/packages/arduino/tools/avrdude/6.3.0-arduino17/bin/avrdude -C/home/nube/.arduino15/packages/arduino/tools/avrdude/6.3.0-arduino17/etc/avrdude.conf -v -patmega328p -carduino -P$serial_port -b57600 -D -Uflash:w:/home/nube/Desktop/flash/DROP_V1_6.hex:i

    avrdude -v -patmega328p -carduino -P$serial_port -b57600 -D -Uflash:w:DROP_V1_6.hex:i
    exit 0
    #sleep 1
    #timeout 15s pyserial-miniterm $serial_port 38400
    #echo "Enter to flash another"
}

yeet



#while read -r line; do
#    yeet
#done
