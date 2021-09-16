from marshmallow import Schema, fields

class Tsl2561:
    def __init__(self, lux):
        self.lux = lux

class Tsl2561Schema(Schema):
    lux = fields.Str()