from app.models.switch_bot.request.device_command import DeviceCommand, DeviceCommandSchema

import requests

class SwitchbotRepository:
    def __init__(self, token):
        self.__domain = 'https://api.switch-bot.com'
        self.__version = 'v1.0'
        self.__headers = {'Authorization': token}
        self.__schema = DeviceCommandSchema()

    def fetch_devices(self):
        url = '/'.join([self.__domain, self.__version, 'devices'])
        result = requests.get(url=url, headers=self.__headers)
        return result.json()

    def fetch_device_status(self, device_id):
        url = '/'.join([self.__domain, self.__version, 'devices', f'{device_id}', 'status'])
        result = requests.get(url=url, headers=self.__headers)
        return result.json()

    def turn_on_device(self, device_id):
        self.__headers['Content-Type'] = 'application/json; charset=utf8'
        url = '/'.join([self.__domain, self.__version, 'devices', f'{device_id}', 'commands'])
        device_command = DeviceCommand(command='turnOn',
                                       parameter='default',
                                       command_type='')
        data = self.__schema.dumps(device_command)
        result = requests.post(url=url, data=data, headers=self.__headers)
        return result.json()

    def turn_off_device(self, device_id):
        self.__headers['Content-Type'] = 'application/json; charset=utf8'
        url = '/'.join([self.__domain, self.__version, 'devices', f'{device_id}', 'commands'])
        device_command = DeviceCommand(command='turnOff',
                                       parameter='default',
                                       command_type='command')
        data = self.__schema.dumps(device_command)
        result = requests.post(url=url, data=data, headers=self.__headers)
        return result.json()

    def setup_aircon(self, device_id, temp, is_cool_mode, is_turn_on):
        self.__headers['Content-Type'] = 'application/json; charset=utf8'
        url = '/'.join([self.__domain, self.__version, 'devices', f'{device_id}', 'commands'])
        mode = 2 if is_cool_mode else 5         # cool or heat
        power_state = 'on' if is_turn_on else 'off'
        device_command = DeviceCommand(command='setAll',
                                       parameter=f'{temp},{mode},1,{power_state}',
                                       command_type='command')
        data = self.__schema.dumps(device_command)
        result = requests.post(url=url, data=data, headers=self.__headers)
        return result.json()