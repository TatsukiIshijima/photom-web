import os
import requests
import uuid

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from PIL import Image
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'JPG', 'JPEG'])

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/photom.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
ma = Marshmallow(app)

from models.photo import *
from models.result import *

result_schema = ResultSchema()

@app.route('/', methods=['GET'])
def index():
    result = photo_list()
    return render_template('index.html', photos=result['photos'])

@app.route('/photo/list', methods=['GET'])
def photo_list():
    photos = Photo.query.all()
    photos_schema = PhotoSchema(many=True)
    result = photos_schema.dump(photos)
    return {'photos': result}

@app.route('/photo/upload', methods=['POST'])
def photo_upload():

    result = Result(Data(1, 'Unknown error.'))

    # 画像保存
    if 'img_file' not in request.files:
        result.data.description = 'file not exist.'
        return result_schema.dump(result)

    img_file = request.files['img_file']
    
    if img_file.filename == '':
        result.data.description = 'file is empty.'
        return result_schema.dump(result)

    if not __is_allowed_extension(img_file.filename):
        result.data.description = 'invalid extension.'
        return result_schema.dump(result)

    filename = secure_filename(img_file.filename)
    _, ext = os.path.splitext(filename)
    filename = str(uuid.uuid4()) + ext
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img_file.save(path)

    # リサイズ
    # FIXME: アスペクト維持
    img = Image.open(path)
    img_resize = img.resize((800, 480))
    img_resize.save(path)

    # DB 書き込み
    photo = Photo(url=os.path.join('http://0.0.0.0:5000/', path))
    db.session.add(photo)
    db.session.commit()

    result.data.code = 0
    result.data.description = ''
    return result_schema.dump(result)

def __is_allowed_extension(file_name):
    return '.' in file_name and file_name.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/photo/delete/<int:id>', methods=['POST'])
def photo_delete(id):

    result = Result(Data(1, 'Unknown error.'))

    photo = Photo.query.get(id)
    
    if photo is None:
        result.data.description = 'target is none.'
        return result_schema.dump(result)

    # 画像削除
    filename = os.path.basename(photo.url)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(path):
        result.data.description = 'file not exist.'
        return result_schema.dump(result)
    os.remove(path)

    # DB から削除
    db.session.query(Photo).filter(Photo.id == id).delete()
    db.session.commit()

    result.data.code = 0
    result.data.description = ''
    return result_schema.dump(result)

@app.route('/weather', methods=['GET'])
def weather():
    url = 'https://api.openweathermap.org/data/2.5/onecall'
    params = {
        'lat': 42.9849944,
        'lon': 140.967782,
        'execlude': 'minutely',
        'units': 'metric',
        'lang': 'ja',
        'appid': 'apikey'
    }
    request = requests.get(url, params)
    return request.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)