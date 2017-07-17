
from flask import Blueprint
from flask_restplus import Api, Resource, fields

# api = Api(blueprint)
apiv2_blueprint = Blueprint('apiv2', __name__, url_prefix='/api/v2')
api = Api(apiv2_blueprint, title='My Title',version='2.0',description='A description',
# All API metadatas
)
from .apis.auth import api as ns1
api.add_namespace(ns1)

@api.route('/hello')
class HelloUganda(Resource):
    def get(self):
        return {'hello':'world'}
