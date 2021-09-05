from models.photo import *
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/photom.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    # DB 書き込み
    # photo = Photo(url='hogehoge')
    # db.session.add(photo)
    # db.session.commit()
    return render_template('index.html')

if __name__ == "__main__":
    # DB 作成
    # db.create_all()
    app.run(host="0.0.0.0", debug=True)