import os
from flask import Flask
from .config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config.from_object(app_config[os.getenv("APP_ENV") or "development"])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# CORS(app,support_credentials=True)

db = SQLAlchemy(app)


