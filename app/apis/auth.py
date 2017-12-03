from flask_restplus import Namespace, Resource, fields, reqparse
from flask import request, jsonify, make_response, g, url_for
import json
from functools import wraps
from app.models import Bucketlist, Item, User
from app import db
from datetime import datetime, date
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()

api = Namespace('auth',
                description='User Authentication')

user_registration = api.model('UserRegistration', {
                    'username': fields.String(required=True,
                            description = "The User's name"),
                    'password': fields.String(required=True,
                            description = "The User's password")
                    })


parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')

@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@api.route('/register/')
class RegisterAPI(Resource):
    """This resource is used to manage user registration"""
    @api.expect(user_registration)
    def post(self):
        """This method is used to register users.
        :@params username: users username
        :@params password: users password
        """
        args = parser.parse_args()
        username = args.username
        password = args.password
        if not username or not password:
            return {'message': "Username and password must be supplied"}, 400
        
        if User.query.filter_by(username = username).first() is not None:
            return {'message' : 'User already exists'}, 400

        user = User(username.strip())
        user.hash_password(password.strip())
        db.session.add(user)
        db.session.commit()
        return {'message' : 'user created succesfully'},200

@api.route('/login/')
class LoginAPI(Resource):
    """This resource is used to handle use login"""
    @api.expect(user_registration)
    def post(self):
        """
        This Method Manages User Authentication
        @params username:
        @params password:
        @returns authentication token
        """
        args = parser.parse_args()
        username = args.username
        password = args.password

        if not username or not password:
            return {'message': "Invalid username or password"}, 400

        user = User.query.filter_by(username = username.strip()).first()
        if not user:
            return {'message': "Invalid username provided"}, 400

        if not user.verify_password(password.strip()):
            return {'message': 'Invalid password provided'}
        
        g.user  = user
        token = g.user.generate_auth_token()
        responseObject = {
            'status': 'success',
            'message': 'Successfully logged in.',
            'token': token.decode('ascii')
                    }
        return responseObject, 200

        
