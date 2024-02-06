#!/bin/bash

yeet() {
    avrdude -C /home/testbench/Droplet/avrdude.conf -v -patmega328p -cusbasp -Pusb -e -Ulock:w:0x3F:m -Uefuse:w:0xFD:m -Uhfuse:w:0xDA:m -Ulfuse:w:0xFF:m -Uflash:w:/home/testbench/Droplet/ATmegaBOOT_168_atmega328_pro_8MHz.hex:i -B10
    echo "Flashing device..."
}

yeet

