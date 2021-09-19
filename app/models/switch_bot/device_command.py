from marshmallow import Schema, fields, post_load

class DeviceCommand:
    def __init__(self, command, parameter, command_type):
        self.command = command
        self.parameter = parameter
        self.command_type = command_type

class DeviceCommandSchema(Schema):
    command = fields.Str(required=True)
    parameter = fields.Str(required=True)
    command_type = fields.Str(required=True, data_key='commandType')