from marshmallow import Schema, fields

class Tsl:
    def __init__(self, lux):
        self.lux = lux

class TslSchema(Schema):
    lux = fields.Str()