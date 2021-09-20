from app.models import db
from app.models.photo.photo import Photo, PhotoSchema

import os

class PhotoRepository:
    def __init__(self):
        self.__photos_schema = PhotoSchema(many=True)

    def fetch_photos(self):
        photos = self.__photos_schema.dump(Photo.query.all())
        photos_dict = {'photos': photos}
        return photos_dict

    def upload_photo(self, domain, path):
        photo = Photo(url=os.path.join(domain, path))
        db.session.add(photo)
        db.session.commit()

    def delete_photo(self, index):
        db.session.query(Photo).filter(Photo.id == index).delete()
        db.session.commit()
