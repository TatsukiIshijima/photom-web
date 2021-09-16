from models.tsl2561 import Tsl2561
from models.bme280 import Bme280
# from bme280i2c import BME280I2C
# from tsl2561 import TSL2561
# from tsl2572 import TSL2572

from models.sensor import *

class RpzSensorWrapper:
    def __init__(self):
        self.sensor_schema = SensorSchema()
        
    def measure(self):
        print('hoge')

    def mock_measure(self):
        bme280_ch1 = Bme280(temp=24.8, pressure=1014.5, humidity=65.1)
        bme280_ch2 = Bme280(temp=28.6, pressure=1015.8, humidity=51.9)
        sensor = Sensor(bme280_ch1,
                        bme280_ch2,
                        Tsl2561(lux=45.9))
        return self.sensor_schema.dump(sensor)
        