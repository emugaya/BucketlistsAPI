#  third party imports
from flask import Flask, jsonify
from flask_restplus import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
#local imports
from config import app_config
from app.views.auth import HelloUganda

# db variable initialization
db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
api = Api(app)

# class HelloUganda(Resource):
#     def get(self):
#         return {'hello': 'uganda'}
api.add_resource(HelloUganda, '/v2/')
