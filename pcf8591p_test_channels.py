#!/usr/bin/env python
# Test program for ADC-DAC PCF8591P
# 2016 https://ph0en1x.net

import os
import time
from smbus import SMBus

from raspberry_print import lcd_text

DEV_ADDR = 0x48
adc_channels = {
    'AIN0 foto': 0b1000000, # 0x40 (foto-resistor)
    'AIN1 thermistor': 0b1000001, # 0x41 (thermistor)
    'AIN2 not connected': 0b1000010, # 0x42 (not connected)
    'AIN3 variable resistor': 0b1000011, # 0x43 (variable resistor)
}
dac_channel = 0b1000000 # 0x40

bus = SMBus(1)          # 1 for RPi model B rev.2
tmp = 0

def main():
    while True:
        print_out = ""
        for channel in adc_channels:
            # read value from ADC input
            bus.write_byte(DEV_ADDR, adc_channels[channel])
            bus.read_byte(DEV_ADDR) # read last value
            bus.read_byte(DEV_ADDR) # repeat reading last value
            value = bus.read_byte(DEV_ADDR)
            if channel == 'AIN3 variable resistor':
                tmp = value
            print_out = f"Channel {channel} ---> {str(value)}\n"
        # set value in DAC
        bus.write_byte_data(DEV_ADDR, dac_channel, tmp)
        lcd_text(print_out)
        os.system("clear")



if __name__ == '__main__':
    main()
