from marshmallow import Schema, fields

class Bme280:
    def __init__(self, temp, pressure, humidity):
        self.temp = temp
        self.pressure = pressure
        self.humidity = humidity

class Bme280Schema(Schema):
    temp = fields.Str()
    pressure = fields.Str()
    humidity = fields.Str()