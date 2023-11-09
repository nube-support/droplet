#!/bin/bash

yeet() {
    #/home/nube/.arduino15/packages/arduino/tools/avrdude/6.3.0-arduino17/bin/avrdude -C/home/nube/.arduino15/packages/arduino/tools/avrdude/6.3.0-arduino17/etc/avrdude.conf -v -B10 -patmega328p -cusbasp -Pusb -e -Ulock:w:0x3F:m -Uefuse:w:0xFD:m -Uhfuse:w:0xDA:m -Ulfuse:w:0xFF:m

    avrdude -C /home/testbench/Droplet/avrdude.conf -v -patmega328p -cusbasp -Pusb -e -Ulock:w:0x3F:m -Uefuse:w:0xFD:m -Uhfuse:w:0xDA:m -Ulfuse:w:0xFF:m -Uflash:w:ATmegaBOOT_168_atmega328_pro_8MHz.hex:i -B10
    echo "Enter to flash another"
}

yeet
#while read -r line; do
#    yeet
#done
