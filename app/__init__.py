import os
import sys

sys.path.append(os.getcwd())

from flask import Flask

from app.config import Config
from app.database import DB

def create_app(config_name=None) -> Flask:
    app = Flask(__name__)

    # Set configs
    if config_name:
        app.config.from_object(config[config_name])
    else:
        app.config.from_object(Config)

    DB.init_app(app)
    return app