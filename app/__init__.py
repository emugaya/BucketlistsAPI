import os
#  third party imports

from flask import Flask, jsonify
from flask_restplus import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy

from app.apiv1 import apiv1_blueprint as apiv1
from app.apiv2 import apiv2_blueprint as apiv2
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
    app.register_blueprint(apiv1)
    app.register_blueprint(apiv2)

    return app





#
#
#
#
#
#
# from config import app_config
# # from app.views.auth import HelloUganda
# #from app.models import *
# from apiv1 import blueprint as api
#
# # app.register_blueprint(api, url_prefix='/api/v1')
#
# # db variable initialization
# db = SQLAlchemy()
# #Create flask app
# app = Flask(__name__)
# #Set Config for the app
# config_name = os.getenv('APP_SETTINGS')
# app.config.from_object('config')
# # app.config.from_object(app_config[config_name])
# #Create BucketList Flask API
# api = Api(app)
#
# @api.route('/v3/')
# class HelloUganda(Resource):
#     def get(self):
#         return 'Hello'
# #Add Resources to buckelist api
# # api.add_resource(HelloUganda, '/v3/')
# # app.register_blueprint(api, url_prefix='/api/v1')
