import json
import requests

class SwitchbotRepository:
    def __init__(self, token):
        self.__domain = 'https://api.switch-bot.com'
        self.__version = 'v1.0'
        self.__headers = {'Authorization': token}

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
        payload = {'command': 'turnOn',
                   'parameter': 'default',
                   'commandType': ''}
        result = requests.post(url=url, data=json.dumps(payload), headers=self.__headers)
        return result.json()

    def turn_off_device(self, device_id):
        self.__headers['Content-Type'] = 'application/json; charset=utf8'
        url = '/'.join([self.__domain, self.__version, 'devices', f'{device_id}', 'commands'])
        payload = {'command': 'turnOff',
                   'parameter': 'default',
                   'commandType': 'command'}
        result = requests.post(url=url, data=json.dumps(payload), headers=self.__headers)
        return result.json()

    def setup_aircon(self, device_id, temp, is_cool_mode, is_turn_on):
        self.__headers['Content-Type'] = 'application/json; charset=utf8'
        url = '/'.join([self.__domain, self.__version, 'devices', f'{device_id}', 'commands'])
        mode = 2 if is_cool_mode else 5         # cool or heat
        power_state = 'on' if is_turn_on else 'off'
        payload = {'command': 'setAll',
                   'parameter': f'{temp},{mode},1,{power_state}',
                   'commandType': 'command'}
        result = requests.post(url=url, data=json.dumps(payload), headers=self.__headers)
        return result.json()