from app.models.rpz_sensor.bme280 import Bme280
from app.models.rpz_sensor.tsl import Tsl
from marshmallow import Schema, fields, post_load

import statistics

def make_from(bme280ch1: Bme280, bme280ch2: Bme280, tsl2572: Tsl):
    temp, pressure, humidity, lux = 0.0, 0.0, 0.0, 0.0

    if bme280ch1 and bme280ch2:
        temp = statistics.median([bme280ch1.temp, bme280ch2.temp])
        pressure = statistics.median([bme280ch1.pressure, bme280ch2.pressure])
        humidity = statistics.median([bme280ch1.humidity, bme280ch2.humidity])
    # Rev2.0 のため TSL2572 のみ対応
    if tsl2572:
        lux = tsl2572.lux

    return Sensor(temp, pressure, humidity, lux)

class Sensor:
    def __init__(self, temp, pressure, humidity, lux):
        self.temp = temp
        self.pressure = pressure
        self.humidity = humidity
        self.lux = lux

class SensorSchema(Schema):
    temp = fields.Float(required=True)
    pressure = fields.Float(required=True)
    humidity = fields.Float(required=True)
    lux = fields.Float(required=True)

    @post_load
    def make_sensor(self, data, **kwargs):
        return Sensor(**data)