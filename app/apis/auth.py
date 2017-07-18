from flask_restplus import Namespace, Resource, fields, reqparse
from flask import request, jsonify, make_response
import json
from app.models import Bucketlist, Item
from app import db
from datetime import datetime, date

api = Namespace('auth',
                description='Create, Read, Update, Display Buckets and Items')
