import private_config

class Config:
    DEBUG = False
    DEVELOPMENT = False
    HOST_NAME = 'raspberrypi-zero.local:5000'
    JSON_AS_ASCII = False
    OPEN_WEATHER_API_KEY = private_config.OPEN_WEATHER_API_KEY
    SECRET_KEY = private_config.SECRET_KEY
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/photom.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWITCH_BOT_TOKEN = private_config.SWITCH_BOT_TOKEN
    UPLOAD_FOLDER = 'static/uploads'

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True