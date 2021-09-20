from app.models import db
from datetime import datetime
from marshmallow import Schema, fields, post_load

class Photo(db.Model):
    __tablename__ = "Photos"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

class PhotoSchema(Schema):
    id = fields.Int()
    url = fields.Str()
    created_at = fields.DateTime()

    @post_load
    def make_photo(self, data, **kwargs):
        return Photo(**data)
