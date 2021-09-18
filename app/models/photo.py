from app.models import db
from datetime import datetime
from marshmallow import Schema, fields

class Photo(db.Model):
    __tablename__ = "Photos"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

class PhotoSchema(Schema):
    id = fields.Int(dump_only=True)
    url = fields.Str()
    created_at = fields.DateTime(dump_only=True)
