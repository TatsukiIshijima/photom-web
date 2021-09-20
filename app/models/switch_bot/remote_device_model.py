from app.models.switch_bot.response.remote_device import RemoteDevice

def make_from(remote_device: RemoteDevice):
    icon_file = ''
    if 'Fan' in remote_device.remote_type:
        icon_file = 'fan_icon.png'
    elif 'Air Conditioner' in remote_device.remote_type:
        icon_file = 'aircon_icon.png'
    elif 'Light' in remote_device.remote_type:
        icon_file = 'light_icon.png'
    return RemoteDeviceModel(remote_device.device_id,
                             remote_device.device_name,
                             remote_device.hub_id,
                             icon_file)

class RemoteDeviceModel:
    def __init__(self, device_id: str, device_name: str, hub_id: str, icon_file: str):
        self.device_id = device_id
        self.device_name = device_name
        self.hub_id = hub_id
        self.icon_file = icon_file