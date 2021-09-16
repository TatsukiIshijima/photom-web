from marshmallow import Schema, fields
from models.tsl2561 import Tsl2561Schema
from models.bme280 import Bme280Schema

class Sensor:
    def __init__(self, bme280_ch1, bme280_ch2, tsl2561):
        self.bme280_ch1 = bme280_ch1
        self.bme280_ch2 = bme280_ch2
        self.tsl2561 = tsl2561

class SensorSchema(Schema):
    bme280_ch1 = fields.Nested(Bme280Schema())
    bme280_ch2 = fields.Nested(Bme280Schema())
    tsl2561 = fields.Nested(Tsl2561Schema())