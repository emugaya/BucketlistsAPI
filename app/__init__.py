#  third party imports
from flask import Flask, jsonify
from flask_restplus import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
#local imports
from config import app_config
from app.views.auth import HelloUganda
from app.models import *

# db variable initialization
db = SQLAlchemy()
#Create flask app
app = Flask(__name__)
#Set Config for the app
app.config.from_object('config')
db.init_app(app)
#Create BucketList Flask API
api = Api(app)

#Add Resources to buckelist api
api.add_resource(HelloUganda, '/v2/')
