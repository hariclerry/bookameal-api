import os
from flask import Flask
from .config import app_config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bookameal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config.from_object(app_config[os.getenv("APP_ENV") or "development"])
