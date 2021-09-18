from flask import Blueprint, current_app, render_template
from app.models.result import Result, ResultSchema, Data
from app.models.sensor import SensorSchema
from app.repositories.sensor_repository import SensorRepository
from app.repositories.weather_repository import WeatherRepository
from app.util import is_content_type_json

import statistics

app = Blueprint('switchbot', __name__, template_folder='templates')
sensor_repository = SensorRepository()
result_schema = ResultSchema()
sensor_schema = SensorSchema()

@app.route('/switchbot', methods=['GET'])
def switch_bot():

    sensor_data = sensor_repository.fetch_mock_sensor_data()

    if not is_content_type_json():
        temp = 0.0
        pressure = 0.0
        humidity = 0.0
        lux = 0.0

        if sensor_data.bme280_ch1 and sensor_data.bme280_ch2:
            temp = statistics.median([sensor_data.bme280_ch1.temp, sensor_data.bme280_ch2.temp])
            pressure = statistics.median([sensor_data.bme280_ch1.pressure, sensor_data.bme280_ch2.pressure])
            humidity = statistics.median([sensor_data.bme280_ch1.humidity, sensor_data.bme280_ch2.humidity])
        # Rev2.0 のため TSL2572 のみ対応
        if sensor_data.tsl2572:
            lux = sensor_data.tsl2572.lux
        return render_template('switch_bot.html',
                               temp='{:.1f}'.format(temp),
                               pressure='{:.1f}'.format(pressure),
                               humidity='{:.1f}'.format(humidity),
                               lux='{:.1f}'.format(lux))
    else:
        if sensor_data is not None:
            return sensor_schema.dump(sensor_data)
        else:
            return sensor_schema.dump(Result(Data(1, '利用可能なセンサーがありません。')))

@app.route('/sensor', methods=['GET'])
def sensor():
    sensor_data = sensor_repository.fetch_mock_sensor_data()
    if sensor_data is not None:
        return sensor_schema.dump(sensor_data)
    else:
        return result_schema.dump(Result(Data(1, '利用可能なセンサーがありません。')))

@app.route('/weather', methods=['GET'])
def weather():
    weather_repository = WeatherRepository(apikey=current_app.config['OPEN_WEATHER_API_KEY'])
    return weather_repository.fetch_weather()