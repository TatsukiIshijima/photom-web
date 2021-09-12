import os
import requests
import uuid

from flask import Flask, abort, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from PIL import Image
from werkzeug.utils import redirect, secure_filename

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

def __is_content_type_json(request):
    return request.headers.get('Content-Type') == 'application/json'

def __is_allowed_extension(file_name):
    return '.' in file_name and file_name.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return photo_list()

@app.route('/photo/list', methods=['GET'])
def photo_list():
    photo_dict = __fetch_photo_list()
    if not __is_content_type_json(request):
        return render_template('index.html', photos=photo_dict['photos'])
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
            return redirect(url_for('index'))

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
            return redirect(url_for('index'))

    # 画像削除
    filename = os.path.basename(photo.url)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(path):
        return abort(500, 'file not exist in upload folder.')
    os.remove(path)

    # DB から削除
    db.session.query(Photo).filter(Photo.id == id).delete()
    db.session.commit()

    if __is_content_type_json(request):
        return result_schema.dump(result)
    else:
        return redirect(url_for('index'))

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