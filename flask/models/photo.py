from datetime import datetime
from app import db

class Photo(db.Model):
    __tablename__ = "Photos"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)