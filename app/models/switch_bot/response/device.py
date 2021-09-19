from marshmallow import Schema, fields, post_load

class Device:
    def __init__(self, device_id: str, device_name: str, device_type: str, hub_id: str):
        self.device_id = device_id
        self.device_name = device_name
        self.device_type = device_type
        self.hub_id = hub_id

class DeviceSchema(Schema):
    device_id = fields.Str(required=True, data_key='deviceId')
    device_name = fields.Str(required=True, data_key='deviceName')
    device_type = fields.Str(required=True, data_key='deviceType')
    hub_id = fields.Str(required=True, data_key='hubDeviceId')

    @post_load
    def make_device(self, data, **kwargs):
        return Device(**data)