import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

from config import Config
from flask import Flask
from flask_bootstrap import Bootstrap5 as Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"
bootstrap = Bootstrap(app)

from app import disney_models, errors, models
from app.routes import disney_routes, main_routes

if not app.debug:
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler(
        "logs/flaskapp.log", maxBytes=10240, backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("RylanSturm.com startup")

# create uploads folder if needed
if not os.path.exists(app.config["UPLOAD_PATH"]):
    os.mkdir(app.config["UPLOAD_PATH"])
