from flask import Blueprint, jsonify
from flask_restplus import Api, Resource, fields

# api = Api(blueprint)
apiv1_blueprint = Blueprint('apiv1', __name__, url_prefix='/api/v1')
api = Api(apiv1_blueprint, title='Bucket Application API',version='1.0',
description="An API to manage bucket lists and their respective items"
# All API metadatas
)

#Register namespace for Managing Buckets Lists and there Items
from .apis.bucketlist import api as ns1
api.add_namespace(ns1)
