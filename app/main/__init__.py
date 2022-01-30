from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import logging

from .config import config_by_name

flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    cfg = config_by_name[config_name]
    app.config.from_object(cfg)
    cfg.init_logging()
    flask_bcrypt.init_app(app)
    CORS(app)

    return app
