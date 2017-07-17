import os
#  third party imports

from flask import Flask, jsonify
from flask_restplus import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy

from config import app_config

# db variable initialization
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__,instance_relative_config=True)
    # config_name = os.getenv('APP_SETTINGS')
    app.config.from_object('config')
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from app.apiv1 import apiv1_blueprint as apiv1
    app.register_blueprint(apiv1)
    from app.apiv2 import apiv2_blueprint as apiv2
    app.register_blueprint(apiv2)

    return app
