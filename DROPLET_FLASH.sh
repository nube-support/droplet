#!/bin/bash

port_number=1
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
    avrdude -v -patmega328p -carduino -P$serial_port -b57600 -D -Uflash:w:/home/testbench/Droplet/DROP_V1_6.hex:i
    exit 0
}

yeet
