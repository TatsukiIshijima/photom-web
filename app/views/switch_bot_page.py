from flask import abort, Blueprint, current_app, render_template, redirect, request, url_for
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

@app.route('/switchbot/aircon/<string:id>', methods=['POST'])
def switch_bot_aircon(id):

    switch_bot_repository = SwitchbotRepository(token=current_app.config['SWITCH_BOT_TOKEN'])

    if request.is_json:
        json = request.get_json()
        if json is None:
            return abort(400)
        temp = json.get('temp')
        is_cool_mode = json.get('is_cool_mode')
        is_turn_on = json.get('is_turn_on')
        if temp is None or is_cool_mode is None or is_turn_on is None:
            return abort(400)
        return switch_bot_repository.setup_aircon(device_id=id, temp=temp, is_cool_mode=is_cool_mode, is_turn_on=is_turn_on)
    else:
        power_button_value = request.form.get('power_button')
        if power_button_value is None:
            abort(500, 'Not define power_button')

        temp = request.form.get('rangeInput')
        is_cool_mode = request.form.get('options-outlined') == 0

        if power_button_value == 'On':
            switch_bot_repository.setup_aircon(device_id=id, temp=temp, is_cool_mode=is_cool_mode, is_turn_on=True)
        elif power_button_value == 'Off':
            switch_bot_repository.setup_aircon(device_id=id, temp=temp, is_cool_mode=is_cool_mode, is_turn_on=False)
        else:
            abort(500, 'Unknown value')

        return redirect(url_for('switchbot.switch_bot'))

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