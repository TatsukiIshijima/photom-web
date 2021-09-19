from flask import abort, Blueprint, current_app, render_template, request
from app.models.rpz_sensor.sensor import SensorSchema
from app.repositories.sensor_repository import SensorRepository
from app.repositories.switch_bot_repository import SwitchbotRepository
from app.repositories.weather_repository import WeatherRepository
from app.util import is_content_type_json

app = Blueprint('switchbot', __name__, template_folder='templates')

@app.route('/switchbot', methods=['GET'])
def switch_bot():
    sensor_repository = SensorRepository()
    sensor_data = sensor_repository.fetch_mock_sensor_data()

    if not is_content_type_json():
        return render_template('switch_bot.html',
                               temp='{:.1f}'.format(sensor_data.temp),
                               pressure='{:.1f}'.format(sensor_data.pressure),
                               humidity='{:.1f}'.format(sensor_data.humidity),
                               lux='{:.1f}'.format(sensor_data.lux))
    else:
        sensor_schema = SensorSchema()
        return sensor_schema.dump(sensor_data)

@app.route('/switchbot/devices', methods=['GET'])
def switch_bot_devices():
    switch_bot_repository = SwitchbotRepository(token=current_app.config['SWITCH_BOT_TOKEN'])
    return switch_bot_repository.fetch_devices()

@app.route('/switchbot/<string:id>/turn_on', methods=['POST'])
def switch_bot_turn_on(id):
    switch_bot_repository = SwitchbotRepository(token=current_app.config['SWITCH_BOT_TOKEN'])
    return switch_bot_repository.turn_on_device(id)

@app.route('/switchbot/<string:id>/turn_off', methods=['POST'])
def switch_bot_turn_off(id):
    switch_bot_repository = SwitchbotRepository(token=current_app.config['SWITCH_BOT_TOKEN'])
    return switch_bot_repository.turn_off_device(id)

# @app.route('/switchbot/<string:id>/aircon_command', methods=['POST'])
# def switch_bot_aircon(id):
#     payload = request.get_data()
#     return type(payload)
#     if not ('temp' in payload and 'is_cool_mode' in payload and 'is_turn_on' in payload):
#         return abort(400)
    temp = payload['temp']
    is_cool_mode = payload['is_cool']
    is_turn_on = payload['is_turn_on']
    # return payload
    # switch_bot_repository = SwitchbotRepository(token=current_app.config['SWITCH_BOT_TOKEN'])
    # return switch_bot_repository.setup_aircon(device_id=id, temp=temp, is_cool_mode=is_cool_mode, is_turn_on=is_turn_on)

@app.route('/sensor', methods=['GET'])
def sensor():
    return switch_bot()

@app.route('/weather', methods=['GET'])
def weather():
    weather_repository = WeatherRepository(apikey=current_app.config['OPEN_WEATHER_API_KEY'])
    return weather_repository.fetch_weather()