from marshmallow import Schema, fields

class Data:
    def __init__(self, code, description):
        self.code = code
        self.description = description

class Result:
    def __init__(self, data):
        self.data = data

class DataSchema(Schema):
    code = fields.Integer()
    description = fields.Str()

class ResultSchema(Schema):
    data = fields.Nested(DataSchema())