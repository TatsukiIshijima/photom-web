from flask import Blueprint, current_app, render_template, redirect, url_for
from app.models.rpz_sensor.sensor import SensorSchema
from app.models.switch_bot.remote_device_model import make_from
from app.models.switch_bot.response.devices import DevicesSchema
from app.repositories.sensor_repository import SensorRepository
from app.repositories.switch_bot_repository import SwitchbotRepository
from app.repositories.weather_repository import WeatherRepository
from app.util import is_content_type_json

app = Blueprint('switchbot', __name__, template_folder='templates')

@app.route('/switchbot', methods=['GET'])
def switch_bot():
    sensor_response = sensor()
    sensor_schema = SensorSchema()
    sensor_data = sensor_schema.load(sensor_response)

    devices_response = switch_bot_devices()
    devices_schema = DevicesSchema()
    devices = devices_schema.load(devices_response)

    remote_device_list = list(map(make_from, devices.body.remote_device_list))

    return render_template('switch_bot.html',
                           temp='{:.1f}'.format(sensor_data.temp),
                           pressure='{:.1f}'.format(sensor_data.pressure),
                           humidity='{:.1f}'.format(sensor_data.humidity),
                           lux='{:.1f}'.format(sensor_data.lux),
                           remote_devices=remote_device_list)

@app.route('/switchbot/devices', methods=['GET'])
def switch_bot_devices():
    switch_bot_repository = SwitchbotRepository(token=current_app.config['SWITCH_BOT_TOKEN'])
    return switch_bot_repository.fetch_devices()

@app.route('/switchbot/<string:id>/turn_on', methods=['POST'])
def switch_bot_turn_on(id):
    switch_bot_repository = SwitchbotRepository(token=current_app.config['SWITCH_BOT_TOKEN'])
    turn_on_response = switch_bot_repository.turn_on_device(id)
    if is_content_type_json():
        return turn_on_response
    else:
        return redirect(url_for('switchbot.switch_bot'))

@app.route('/switchbot/<string:id>/turn_off', methods=['POST'])
def switch_bot_turn_off(id):
    switch_bot_repository = SwitchbotRepository(token=current_app.config['SWITCH_BOT_TOKEN'])
    turn_off_response = switch_bot_repository.turn_off_device(id)
    if is_content_type_json():
        return turn_off_response
    else:
        return redirect(url_for('switchbot.switch_bot'))

# @app.route('/switchbot/<string:id>/aircon_command', methods=['POST'])
# def switch_bot_aircon(id):
#     payload = request.get_data()
#     return type(payload)
#     if not ('temp' in payload and 'is_cool_mode' in payload and 'is_turn_on' in payload):
#         return abort(400)
#     temp = payload['temp']
#     is_cool_mode = payload['is_cool']
#     is_turn_on = payload['is_turn_on']
    # return payload
    # switch_bot_repository = SwitchbotRepository(token=current_app.config['SWITCH_BOT_TOKEN'])
    # return switch_bot_repository.setup_aircon(device_id=id, temp=temp, is_cool_mode=is_cool_mode, is_turn_on=is_turn_on)

@app.route('/sensor', methods=['GET'])
def sensor():
    sensor_repository = SensorRepository()
    sensor_schema = SensorSchema()
    sensor_data = sensor_repository.fetch_mock_sensor_data()
    return sensor_schema.dump(sensor_data)

@app.route('/weather', methods=['GET'])
def weather():
    weather_repository = WeatherRepository(apikey=current_app.config['OPEN_WEATHER_API_KEY'])
    return weather_repository.fetch_weather()