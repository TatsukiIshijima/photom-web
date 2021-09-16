#!/usr/bin/env python3

"""
RPZ-IR-Sensor BME280 and TSL2561 Controller
Usage:
    rpz_sensor.py [-l <log_file>] [-v]
    rpz_sensor.py -h --help

Options:
    -l <log_file>  Output log file name
    -v             Show verbose message
    -h --help      Show this screen and exit
"""

import os
import csv
from bme280i2c import BME280I2C
from tsl2561 import TSL2561
from tsl2572 import TSL2572
from datetime import datetime
from docopt import docopt

def main():
    args = docopt(__doc__)
    loglist = ['']*8

    bme280ch1 = BME280I2C(0x76)
    bme280ch2 = BME280I2C(0x77)
    tsl2561 = TSL2561(0x29)
    tsl2572 = TSL2572(0x39)
    r1 = bme280ch1.meas()
    r2 = bme280ch2.meas()
    r3 = tsl2561.meas_single()
    r4 = tsl2572.meas_single()

    if not (r1 or r2 or r3):
        print('No Sensor Available')

    if r1:
        print('BME280 0x76')
        if args['-v']:
            bme280ch1.print_cal()
            bme280ch1.print_reg()
        bme280ch1.print_meas()
        loglist[1] = '{:.1f}'.format(bme280ch1.T)
        loglist[3] = '{:.1f}'.format(bme280ch1.P)
        loglist[5] = '{:.1f}'.format(bme280ch1.H)

    if r2:
        if r1:
            print()
        print('BME280 0x77')
        if args['-v']:
            bme280ch2.print_cal()
            bme280ch2.print_reg()
        bme280ch2.print_meas()
        loglist[2] = '{:.1f}'.format(bme280ch2.T)
        loglist[4] = '{:.1f}'.format(bme280ch2.P)
        loglist[6] = '{:.1f}'.format(bme280ch2.H)

    if r3:
        if r1 or r2:
            print()
        print('TSL2561')
        if args['-v']:
            tsl2561.print_reg()
        tsl2561.print_meas()
        loglist[7] = '{:.1f}'.format(tsl2561.lux)

    if r4:
        if r1 or r2:
            print()
        print('TSL2572')
        if args['-v']:
            tsl2572.print_reg()
        tsl2572.print_meas()
        loglist[7] = '{:.1f}'.format(tsl2572.lux)

    if args['-l'] != None:
        exist = os.path.isfile(args['-l'])

        with open(args['-l'], 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            if not exist:
                writer.writerow(['Time', 'Temp ch1', 'Temp ch2', 'Pressure ch1',
                    'Pressure ch2', 'Humidity ch1', 'Humidity ch2', 'Lux'])
        
            datestr = datetime.now().strftime("%Y/%m/%d %H:%M")
            loglist[0] = datestr
            writer.writerow(loglist)

if __name__ == '__main__':
    main()


