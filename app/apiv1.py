from flask import Blueprint, jsonify, request
from flask_restplus import Api, Resource, fields
from flask_cors import CORS, cross_origin


# Set up API Blueprint for version V1
apiv1_blueprint = Blueprint('apiv1', __name__, url_prefix='/api/v1')
api = Api(apiv1_blueprint, title='Bucket List Application API',version='1.0',
description="An API to manage bucket lists and their respective items"
# All API metadatas
        )
#Register namespace for managing User Login and registration
from .apis.auth import api as ns1
api.add_namespace(ns1)

#Register namespace for Managing Buckets Lists and there Items
from .apis.bucketlist import api as ns2
api.add_namespace(ns2)
