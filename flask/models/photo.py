from datetime import datetime
from app import db
from app import ma

class Photo(db.Model):
    __tablename__ = "Photos"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

class PhotoScheme(ma.Schema):
    class Meta:
        # fields で値を変更可能
        fields = ("id", "url", "created_at")
