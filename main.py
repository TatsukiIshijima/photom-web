from app import create_app, db

"""
# 以下の import はスクリプト上で
# 参照されていないが DB を作成するのに必要
"""
from app.models.photo.photo import Photo

photom_app = create_app()

if __name__ == '__main__':
    db.create_all(app=photom_app)
    photom_app.run(host='0.0.0.0')