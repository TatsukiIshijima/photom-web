from marshmallow import Schema, fields, post_load

class RemoteDevice:
    def __init__(self, device_id: str, device_name: str, hub_id: str, remote_type: str):
        self.device_id = device_id
        self.device_name = device_name
        self.hub_id = hub_id
        self.remote_type = remote_type

class RemoteDeviceSchema(Schema):
    device_id = fields.Str(required=True, data_key='deviceId')
    device_name = fields.Str(required=True, data_key='deviceName')
    hub_id = fields.Str(required=True, data_key='hubDeviceId')
    remote_type = fields.Str(required=True, data_key='remoteType')

    @post_load
    def make_remote_device(self, data, **kwargs):
        return RemoteDevice(**data)