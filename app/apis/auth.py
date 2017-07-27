from flask_restplus import Namespace, Resource, fields, reqparse
from flask import request, jsonify, make_response
import json
from app.models import Bucketlist, Item, User
from app import db
from datetime import datetime, date

api = Namespace('auth',
                description='User Authentication')

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')

# @api.route('/login')
# def login(self):
#     pass
#
# @api.route('/register')
# def register(self):
#     pass
