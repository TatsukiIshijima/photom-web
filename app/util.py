from flask import request

def is_allowed_extension(file_name):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'JPG', 'JPEG'}
    return '.' in file_name and file_name.rsplit('.', 1)[1] in allowed_extensions