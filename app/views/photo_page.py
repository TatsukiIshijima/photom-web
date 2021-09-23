from app.repositories.photo_repository import PhotoRepository
from app.models.photo.photo import Photo
from app.models.result import Result, ResultSchema, Data
from app.util import is_allowed_extension
from flask import abort, Blueprint, current_app, flash, render_template, redirect, request, url_for
from PIL import Image
from werkzeug.utils import secure_filename

import os
import uuid

app = Blueprint('photo', __name__, template_folder='templates')
photo_repository = PhotoRepository()
result_schema = ResultSchema()

@app.route('/')
def index():
    return photo_list()

@app.route('/photo/list', methods=['GET'])
def photo_list():
    photos_response = photo_repository.fetch_photos()
    if not request.is_json:
        return render_template('photo.html', photos=photos_response['photos'])
    else:
        return photos_response

@app.route('/photo/upload', methods=['POST'])
def photo_update():
    result = Result(Data(0, ''))

    # 画像保存
    if 'img_file' not in request.files:
        return abort(500, 'img_file not define.')

    img_file = request.files['img_file']

    if img_file.filename == '':
        result.data.code = 1
        result.data.description = 'ファイルが選択されていません。'

    if not is_allowed_extension(img_file.filename):
        result.data.code = 1
        result.data.description = '無効なファイルです。'

    if result.data.code != 0 and len(result.data.description) != 0:
        if request.is_json:
            return result_schema.dump(result)
        else:
            flash(result.data.description)
            return redirect(url_for('photo.index'))

    filename = secure_filename(img_file.filename)
    _, ext = os.path.splitext(filename)
    filename = str(uuid.uuid4()) + ext
    app_relative_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    app_absolute_path = os.path.join('app', app_relative_path)
    img_file.save(app_absolute_path)

    # リサイズ
    img = Image.open(app_absolute_path)
    # 短辺に合わせてしまうため、800x480 を x1.2 した値を設定
    img.thumbnail(size=(960, 576))
    img.save(app_absolute_path)

    photo_repository.upload_photo(domain= f'http://{current_app.config["HOST_NAME"]}',
                                  path=app_relative_path)

    if request.is_json:
        return result_schema.dump(result)
    else:
        return redirect(url_for('photo.index'))

@app.route('/photo/delete/<int:id>', methods=['POST'])
def photo_delete(id):
    result = Result(Data(0, ''))
    photo = Photo.query.get(id)

    if photo is None:
        result.data.code = 1
        result.data.description = '削除する写真がありません。'
    if result.data.code != 0 and len(result.data.description) != 0:
        if request.is_json:
            return result_schema.dump(result)
        else:
            flash(result.data.description)
            return redirect(url_for('photo.index'))

    # 画像削除
    filename = os.path.basename(photo.url)
    app_absolute_path = os.path.join('app', current_app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(app_absolute_path):
        return abort(500, 'file not exist in upload folder.')
    os.remove(app_absolute_path)

    photo_repository.delete_photo(index=id)

    if request.is_json:
        return result_schema.dump(result)
    else:
        return redirect(url_for('photo.index'))