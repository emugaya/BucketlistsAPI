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
    # Verify Token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
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
        username = args.username.strip()
        password = args.password.strip()
        try:
            if len(username) == 0:
                return {'error_message': "Username and password must be supplied"}
            if len(password) == 0:
                return {'error_message': "Username and password must be supplied"}
            if User.query.filter_by(username = username).first() is not None:
                return {'error_message' : 'User already exists'} # existing user
            user = User(username)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            return {'message' : 'user created succesfully'}
        except:
            return {'error_message':'Ooops.. An error happend during registration try again'}

@api.route('/login')
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
        if len(username) == 0:
            return {'error_message': "Invalid username or password"}
        if len(password) == 0:
            return {'error_message': "Invalid username or password"}
        try:
            user = User.query.filter_by(username = username).first()
            # password = user.hash_password(password)
            print(user.verify_password(password))
            if user.verify_password(password):
                g.user  = user
                token = g.user.generate_auth_token()
                if token:
                    responseObject = {
                        'status': 'success',
                         'message': 'Successfully logged in.',
                         'token': token.decode('ascii')
                         }
                    return responseObject, 200
            else:
                return {'error_message': "Invalid username or password"}

        except:
            return {'error_message': 'Invalid username or password'}
