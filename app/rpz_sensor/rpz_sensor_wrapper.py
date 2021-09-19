from app.models.rpz_sensor.bme280 import Bme280
from app.models.rpz_sensor.tsl import Tsl
from app.rpz_sensor.bme280i2c import BME280I2C
from app.rpz_sensor.tsl2561 import TSL2561
from app.rpz_sensor.tsl2572 import TSL2572

from app.models.rpz_sensor.sensor import make_from

class RpzSensorWrapper:

    def measure(self):
        bme280_ch1 = None
        bme280_ch2 = None
        tsl_2561 = None
        tsl_2572 = None

        bme280ch1 = BME280I2C(0x76)
        bme280ch2 = BME280I2C(0x77)
        tsl2561 = TSL2561(0x29)
        tsl2572 = TSL2572(0x39)
        r1 = bme280ch1.meas()
        r2 = bme280ch2.meas()
        r3 = tsl2561.meas_single()
        r4 = tsl2572.meas_single()

        if not (r1 or r2 or r3):
            return None
        
        if r1:
            bme280_ch1 = Bme280(temp=bme280ch1.T, pressure=bme280ch1.P, humidity=bme280ch1.H)
        if r2:
            bme280_ch2 = Bme280(temp=bme280ch2.T, pressure=bme280ch2.P, humidity=bme280ch2.H)
        if r3:
            tsl_2561 = Tsl(lux=tsl2561.lux)
        if r4:
            tsl_2572 = Tsl(lux=tsl2572.lux)

        return make_from(bme280_ch1, bme280_ch2, tsl_2572)

    def mock_measure(self):
        bme280ch1 = Bme280(temp=24.8, pressure=1014.5, humidity=65.1)
        bme280ch2 = Bme280(temp=28.6, pressure=1015.8, humidity=51.9)
        tsl2572 = Tsl(lux=45.9)
        return make_from(bme280ch1, bme280ch2, tsl2572)
        