from flask_restplus import Namespace, Resource, fields, reqparse
from flask import request, jsonify, make_response,g
from flask_cors import CORS, cross_origin
from werkzeug.exceptions import BadRequest, Conflict
from sqlalchemy.orm import joinedload
import json
from datetime import datetime, date

from app.models import Bucketlist, dump_datetime
from app import db
from app.routes.auth import auth

# This namespace is used to control CRUD operations for buckets and items
api = Namespace('bucketlists',
                description='Create, Read, Update, Display Buckets and Items')

# This holds the name of bucket being created
bucketlist= api.model('BucketlistPost', {
                    'name': fields.String(required=True,
                            description = "The Bucket List name"),
                    'description': fields.String(description ="Details about the Bucketlist")
                    })

# The parsers below are used to get apylod data from the user
parser = reqparse.RequestParser()
parser.add_argument('bucketlist_id')
parser.add_argument('item_id')
parser.add_argument('name')
parser.add_argument('item_name')
parser.add_argument('done')
parser.add_argument('user_id')

bucket_lists = api.model('Bucketlist', {
                    'id':fields.Integer(description = "Bucket ID"),
                    'name': fields.String(
                            description = "Bucket name"),
                    'description': fields.String(description ="Details about the Bucketlist"),
                    'date_created':fields.DateTime,
                    'date_modified': fields.DateTime,
                    'created_by': fields.Integer(
                            description= "User whoc created this bucket")
                    })
bucket_list_items = api.model('BucketListItems', {
                    'id': fields.Integer(description = "Bucket Item ID"),
                    'name': fields.String(
                            description = "Bucketlist Name"),
                    'description': fields.String(description ="Details about the Item"),
                    'done': fields.Boolean( description = "True or False"),
                    'date_created':fields.DateTime,
                    'date_modified': fields.DateTime,
                    'created_by': fields.Integer(
                            description= "User who created this bucket")
})


#Constants
min_number_of_buckets_per_page = 20
max_number_of_buckets_per_page = 100

# Pagination parsers
pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False,
                                    default=1, help='Page number')
pagination_arguments.add_argument('bool', type=bool, required=False,
                                    default=1, help='Page number')

#Set number of results per page
pagination_arguments.add_argument('per_page', type=int, required=False,
                            default=20, help='Results per page {error_msg}')
pagination_arguments.add_argument('search', type=str, required=False, default = '')

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

page_of_bucket_lists = api.inherit('Page of blog posts', pagination, {
    'items': fields.List(fields.Nested(bucket_lists))
})

@api.route('/')
class BucketLists(Resource):
    """This Resource is used to create buckets and lists all buckets"""
    @api.response(200,'Success')
    @auth.login_required
    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_bucket_lists)
    def get(self):
        """ This method returns buckets created by an individual user."""
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        search = args.get('search','')
        per_page = args.get('per_page', 6)
        if per_page < min_number_of_buckets_per_page:
            per_page = min_number_of_buckets_per_page

        if per_page > max_number_of_buckets_per_page:
            per_page = max_number_of_buckets_per_page

        if search:
            search = search.lower()
            bucket_lists = Bucketlist.query.filter(
                (Bucketlist.created_by == g.user.id),
                (func.lower(Bucketlist.name).like("%"+search+"%"))
                )
        else:
            bucket_lists = Bucketlist.query.filter(Bucketlist.created_by == g.user.id)

        bucket_list_page = bucket_lists.paginate(page, per_page, error_out=False)
        return bucket_list_page, 200

    @api.response(201, 'Success')
    @api.expect(bucketlist)
    @auth.login_required
    def post(self):
        """
        This post method is used to create buckets for a user already logged in.
        :params :name
        :returns :200 for succesful post
        """
        args = parser.parse_args()
        name = args.name.strip()
        created_by = g.user.id
        if not name:
            raise BadRequest('Please provide a name for your bucketlist')

        bucketlist = Bucketlist.query.filter_by(name=name, created_by=created_by).first()
        if bucketlist:
            raise Conflict('Bucket with similar name already exists')

        bucketlist = Bucketlist(name,created_by)
        db.session.add(bucketlist)
        db.session.commit()
        return {'message': 'Bucket list created Successfully'}, 201

@api.route('/<bucketlist_id>')
class SingleBucketlist(Resource):
    """This Resource displays, edits and deleted as single bucket"""
    @auth.login_required
    def get(self, bucketlist_id):
        """
        This method is used to list details of a bucket and it's items
        :params bucketlist_id: id of individaual bucket to retrieved from the db
        :returns - bucketlist and all it's items
        """
        bucketlist = Bucketlist.query.options(joinedload(Bucketlist.items)).filter_by(id = bucketlist_id).first()
        if not bucketlist:
            return {"message": "Bucket " + bucketlist_id + " Doesn't Exist"}, 404
        
        result ={}
        result['id'] = bucketlist.id 
        result['name'] = bucketlist.name
        result['created_by'] = bucketlist.created_by
        result['date_modified'] = dump_datetime(bucketlist.date_modified)
        result['date_created'] = dump_datetime(bucketlist.date_created)
        result['items'] = ([i.serialize for i in bucketlist.items])
        return result , 200

    @api.expect(bucketlist)
    @auth.login_required
    def put(self, bucketlist_id):
        """
        This method is used to edit/ update the name and status of a bucket
        :params bucketlist_id:
        """
        args = parser.parse_args()
        name = args.name

        if not name:
            raise BadRequest("Please provide a new name for your bucketlist")
        bucketlist = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).first()

        if not bucketlist:
            return {"message": "The Buckelist " + bucketlist_id + " provided doesn't exist ...."}, 404

        bucketlist.name = args.name
        db.session.add(bucketlist)
        db.session.commit()
        return {"message": "Bucket list name updated or changed Successfully"}, 204

    @auth.login_required
    def delete(self, bucketlist_id):
        """
        This method is used to delete buckets and there respective items
        :params bucketlist_id: ID of bucket being deleted
        """
        bucketlist = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).first()

        if not bucketlist:
            return {"message": "The Buckelist "+bucketlist_id+ " provided doesn't exist ...."}, 404

        db.session.delete(bucketlist)
        db.session.commit()
        return{"message" : "Bucketlist "+bucketlist_id+" deleted succesfully."}, 201
