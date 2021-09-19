from typing import List
from app.models.switch_bot.response.device import Device, DeviceSchema
from app.models.switch_bot.response.remote_device import RemoteDevice, RemoteDeviceSchema
from marshmallow import Schema, fields, post_load

class Body:
    def __init__(self, device_list: List[Device], remote_device_list: List[RemoteDevice]):
        self.device_list = device_list
        self.remote_device_list = remote_device_list

class BodySchema(Schema):
    device_list = fields.List(fields.Nested(DeviceSchema), required=True, data_key='deviceList')
    remote_device_list = fields.List(fields.Nested(RemoteDeviceSchema), required=True, data_key='infraredRemoteList')

    @post_load
    def make_body(self, data, **kwargs):
        return Body(**data)