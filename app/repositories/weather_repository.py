import requests

class WeatherRepository:
    def __init__(self, apikey, lat=42.9849944, lon=140.967782):
        self.__apikey = apikey
        self.__url = 'https://api.openweathermap.org/data/2.5/onecall'
        self.__lat = lat
        self.__lon = lon

    def fetch_weather(self):
        params = {
            'lat': self.__lat,
            'lon': self.__lon,
            'execlude': 'minutely',
            'units': 'metric',
            'lang': 'ja',
            'appid': self.__apikey
        }
        result = requests.get(self.__url, params)
        return result.json()