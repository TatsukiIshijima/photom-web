from flask import Flask
from app.models import db
from app.views import photo_page, switch_bot_page

import os

def create_app():
    app = Flask(__name__)
    env_config = os.getenv('APP_SETTINGS', 'config.DevelopmentConfig')
    app.config.from_object(env_config)

    db.init_app(app)

    app.register_blueprint(photo_page.app)
    app.register_blueprint(switch_bot_page.app)

    return app