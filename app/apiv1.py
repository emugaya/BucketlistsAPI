from flask import Blueprint, jsonify, request
from flask_restplus import Api, Resource, fields
from flask_cors import CORS, cross_origin


# Set up API Blueprint for version V1
apiv1_blueprint = Blueprint('apiv1', __name__, url_prefix='/api/v1')

api = Api(apiv1_blueprint, 
        title='Bucket List Application API',
        version='1.0',
        description="An API to manage bucket lists and their respective items"
        )

#Register namespace for managing User Login and registration
from .routes.auth import api as auth_namespace
api.add_namespace(auth_namespace)

#Register namespace for Managing Bucketlists
from .routes.bucketlist import api as bucketlist_namespace
api.add_namespace(bucketlist_namespace)

#Register namespace for Manageing Bucketlist Items
from .routes.item import api as item_namesapce
api.add_namespace(item_namesapce)
