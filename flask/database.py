# 初めに Photo クラスを import してから db を import しないとエラーになる
from models.photo import Photo
from app import db

if __name__ == "__main__":
    print(' * Create database')
    db.create_all()