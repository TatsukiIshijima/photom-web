#!/usr/bin/env python3

"""
TSL2561 Control Module via I2C
 2019/1/7
"""

import smbus
import time

class TSL2561:
    AGAIN_LOW = 0
    AGAIN_HIGH = 1

    ATIME_13MS = 0
    ATIME_101MS = 1
    ATIME_402MS = 2

    def __init__(self, i2c_addr):
        self.i2c_addr = i2c_addr
        self.i2c = smbus.SMBus(1)
        self.ch0 = 0
        self.ch1 = 0
        self.lux = 0
        self.again = TSL2561.AGAIN_HIGH
        self.atime = TSL2561.ATIME_402MS

    # I2C read length byte from addr
    def read_address(self, addr, length):
        addr = addr | 0x80
        try:
            return self.i2c.read_i2c_block_data(self.i2c_addr, addr, length)
        except IOError:
            return [0 for i in range(length)]

    # I2C write data to addr
    def write_address(self, addr, data):
        addr = addr | 0x80
        self.i2c.write_i2c_block_data(self.i2c_addr, addr, data)

    # Read ID and return True if success
    def id_read(self):
        data = self.read_address(0xA, 1)
        data[0] = data[0]>>4
        if data[0] == 0x1 or data[0] == 0x5 or data[0] == 0x7:
            return True
        return False

    def set_timing(self, again, atime):
        self.write_address(0x1, [(again<<4) | atime])

    def als_integration(self):
        self.write_address(0x0, [0x0])     # Power OFF
        self.set_timing(self.again, self.atime)
        self.write_address(0x0, [0x3])     # Power ON

        if TSL2561.ATIME_13MS == self.atime:
            time.sleep(0.020)
        elif TSL2561.ATIME_101MS == self.atime:
            time.sleep(0.120)
        elif TSL2561.ATIME_402MS == self.atime:
            time.sleep(0.430)

        data = self.read_address(0xC, 4)
        self.write_address(0x0, [0x0])     # Power OFF
        self.ch0 = (data[1] << 8) | data[0]
        self.ch1 = (data[3] << 8) | data[2]

    def meas_single(self):
        if not self.id_read():
            return False

        self.again = TSL2561.AGAIN_HIGH
        self.atime = TSL2561.ATIME_101MS

        while True:
            self.als_integration()
            if self.ch0 > 37000 or self.ch1 > 37000:
                if self.again == TSL2561.AGAIN_HIGH and self.atime == TSL2561.ATIME_101MS:
                    self.again = TSL2561.AGAIN_LOW
                else:
                    break
            elif self.ch0 < 300 or self.ch1 < 300:
                if self.again == TSL2561.AGAIN_HIGH and self.atime == TSL2561.ATIME_101MS:
                    self.atime = TSL2561.ATIME_402MS
                else:
                    break
            else:
                break
        self.calc_lux()
        return True

    def calc_lux(self):
        if TSL2561.ATIME_13MS == self.atime:
            t = 13.7
        elif TSL2561.ATIME_101MS == self.atime:
            t = 101
        elif TSL2561.ATIME_402MS == self.atime:
            t = 402

        if TSL2561.AGAIN_LOW == self.again:
            g = 1
        elif TSL2561.AGAIN_HIGH == self.again:
            g = 16

        if 0==self.ch0:
            lux = 0
        else:
            ratio = self.ch1 / self.ch0

            # T, FN, CL package
            if ratio <= 0.5:
                lux = 0.0304*self.ch0 - (0.062*self.ch0 * pow(ratio,1.4))
            elif ratio <= 0.61:
                lux = 0.0224*self.ch0 - 0.031*self.ch1
            elif ratio <= 0.8:
                lux = 0.0128*self.ch0 - 0.0153*self.ch1
            elif ratio <=1.3:
                lux = 0.00146*self.ch0 - 0.00112*self.ch1
            else:
                lux = 0

        self.lux = lux * 16/g * 402/t
        
    def print_reg(self):
        if TSL2561.ATIME_13MS == self.atime:
            print(' ADC Time : 13ms')
        elif TSL2561.ATIME_101MS == self.atime:
            print(' ADC Time : 101ms')
        elif TSL2561.ATIME_402MS == self.atime:
            print(' ADC Time : 402ms')

        if TSL2561.AGAIN_LOW == self.again:
            print(' ADC Gain : Low')
        elif TSL2561.AGAIN_HIGH == self.again:
            print(' ADC Gain : High')

        print(' ch0 : 0x{:X}'.format(self.ch0))
        print(' ch1 : 0x{:X}'.format(self.ch1))
        
    
    def print_meas(self):
        print( ' Lux : {:.1f}lux'.format(self.lux))

def main():
    tsl2561 = TSL2561(0x29)
    tsl2561.meas_single()
    tsl2561.print_reg()
    tsl2561.print_meas()

if __name__ == '__main__':
    main()





