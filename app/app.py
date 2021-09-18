import os
import private_config
import requests
import statistics
import uuid

from flask import Flask, abort, flash, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from PIL import Image
from werkzeug.utils import redirect, secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'JPG', 'JPEG'}

app = Flask(__name__)
env_config = os.getenv('APP_SETTINGS', 'config.DevelopmentConfig')
app.config.from_object(env_config)

db = SQLAlchemy(app)
ma = Marshmallow(app)

from models.photo import *
from models.result import ResultSchema, Result, Data
from models.sensor import SensorSchema
from rpz_sensor.rpz_sensor_wrapper import RpzSensorWrapper

result_schema = ResultSchema()
sensor_schema = SensorSchema()

def __is_content_type_json(request):
    return request.headers.get('Content-Type') == 'application/json'

def __is_allowed_extension(file_name):
    return '.' in file_name and file_name.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return photo_list()

@app.route('/switchbot')
def switch_bot():
    
    sensor_data = __get_sensor_data()
    
    if not __is_content_type_json(request):
        
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

@app.route('/photo/list', methods=['GET'])
def photo_list():
    photo_dict = __fetch_photo_list()
    if not __is_content_type_json(request):
        return render_template('photo.html', photos=photo_dict['photos'])
    else :
        return photo_dict

def __fetch_photo_list():
    photos = Photo.query.all()
    photos_schema = PhotoSchema(many=True)
    result = photos_schema.dump(photos)
    photos_dict = {'photos': result}
    return photos_dict

@app.route('/photo/upload', methods=['POST'])
def photo_upload():

    result = Result(Data(0, ''))

    # 画像保存
    if 'img_file' not in request.files:
        return abort(500, 'img_file not define.')

    img_file = request.files['img_file']
    
    if img_file.filename == '':
        result.data.code = 1
        result.data.description = 'ファイルが選択されていません。'

    if not __is_allowed_extension(img_file.filename):
        result.data.code = 1
        result.data.description = '無効なファイルです。'

    if result.data.code != 0 and len(result.data.description) != 0:
        if __is_content_type_json(request):
            return result_schema.dump(result)
        else:
            flash(result.data.description)
            return redirect(url_for('index'))

    filename = secure_filename(img_file.filename)
    _, ext = os.path.splitext(filename)
    filename = str(uuid.uuid4()) + ext
    app_relative_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    app_absolute_path = os.path.join('app', app_relative_path)
    img_file.save(app_absolute_path)

    # リサイズ
    # FIXME: アスペクト維持
    img = Image.open(app_absolute_path)
    img_resize = img.resize((800, 480))
    img_resize.save(app_absolute_path)

    # DB 書き込み
    photo = Photo(url=os.path.join('http://0.0.0.0:5000/', app_relative_path))
    db.session.add(photo)
    db.session.commit()

    if __is_content_type_json(request):
        return result_schema.dump(result)
    else:
        return redirect(url_for('index'))

@app.route('/photo/delete/<int:id>', methods=['POST'])
def photo_delete(id):

    result = Result(Data(0, ''))

    photo = Photo.query.get(id)
    
    if photo is None:
        result.data.code = 1
        result.data.description = '削除する写真がありません。'

    if result.data.code != 0 and len(result.data.description) != 0:
        if __is_content_type_json(request):
            return result_schema.dump(result)
        else:
            flash(result.data.description)
            return redirect(url_for('index'))

    # 画像削除
    filename = os.path.basename(photo.url)
    app_absolute_path = os.path.join('app', app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(app_absolute_path):
        return abort(500, 'file not exist in upload folder.')
    os.remove(app_absolute_path)

    # DB から削除
    db.session.query(Photo).filter(Photo.id == id).delete()
    db.session.commit()

    if __is_content_type_json(request):
        return result_schema.dump(result)
    else:
        return redirect(url_for('index'))

@app.route('/sensor', methods=['GET'])
def sensor():
    sensor_data = __get_sensor_data()
    if sensor_data is not None:
        return sensor_schema.dump(sensor_data)
    else:
        return result_schema.dump(Result(Data(1, '利用可能なセンサーがありません。')))

def __get_sensor_data():
    rpz_sensor = RpzSensorWrapper()
    return rpz_sensor.mock_measure()

@app.route('/weather', methods=['GET'])
def weather():
    url = 'https://api.openweathermap.org/data/2.5/onecall'
    params = {
        'lat': 42.9849944,
        'lon': 140.967782,
        'execlude': 'minutely',
        'units': 'metric',
        'lang': 'ja',
        'appid': app.config.get('OPEN_WEATHER_API_KEY')
    }
    result = requests.get(url, params)
    return result.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0")