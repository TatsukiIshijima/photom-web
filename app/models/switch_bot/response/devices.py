from app.models.switch_bot.response.body import Body, BodySchema
from marshmallow import Schema, fields, post_load

class Devices:
    def __init__(self, body: Body, message: str, status_code: int):
        self.body = body
        self.message = message
        self.status_code = status_code

class DevicesSchema(Schema):
    body = fields.Nested(BodySchema, required=True, data_key='body')
    message = fields.Str(required=True, data_key='message')
    status_code = fields.Int(required=True, data_key='statusCode')

    @post_load
    def make_devices(self, data, **kwargs):
        return Devices(**data)