from flask import Flask, json, render_template, request, redirect, url_for, send_from_directory, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from models.photo import *
from PIL import Image
from werkzeug.utils import secure_filename

import os
import requests
import uuid


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'JPG', 'JPEG'])

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/photom.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # 画像保存
    if 'img_file' not in request.files:
        return make_response(jsonify({'result': {'code': 1, 'description': 'file not exist.'}}))
    img_file = request.files['img_file']
    if img_file.filename == '':
        return make_response(jsonify({'result': {'code': 1, 'description': 'file is empty.'}}))
    if not __is_allowed_extension(img_file.filename):
        return make_response(jsonify({'result': {'code': 1, 'description': 'invalid extension.'}}))
    filename = secure_filename(img_file.filename)
    _, ext = os.path.splitext(filename)
    filename = str(uuid.uuid4()) + ext
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img_file.save(path)

    # リサイズ
    img = Image.open(path)
    img_resize = img.resize((800, 480))
    img_resize.save(path)

    # DB 書き込み
    photo = Photo(url=os.path.join('http://0.0.0.0:5000/', path))
    db.session.add(photo)
    db.session.commit()

    return make_response(jsonify({'result': {'code': 0, 'description': ''}}))

def __is_allowed_extension(file_name):
    return '.' in file_name and file_name.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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
    return make_response(jsonify(request.text))

if __name__ == "__main__":
    # DB 作成
    # db.create_all()
    app.run(host="0.0.0.0", debug=True)