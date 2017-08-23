from flask_restplus import Namespace, Resource, fields, reqparse
from flask import request, jsonify, make_response,g
import json
from app.models import Bucketlist, Item
from app import db
from sqlalchemy import func, Column, Integer, String
from app.apis.auth import auth
from datetime import datetime, date
from flask_cors import CORS, cross_origin
# from app.apis.parsers import pagination_arguments

# This namespace is used to control CRUD operations for buckets and items
api = Namespace('bucketlists',
                description='Create, Read, Update, Display Buckets and Items')
# CORS(api) #S,resources={r"/": {"origins": "*"}},allow_headers = ['Content-Type', 'Authorization'])

# This holds the name of bucket being created
bucketlist_post = api.model('BucketlistPost', {
                    'name': fields.String(required=True,
                            description = "The Bucket List name")
                    })
# This holds the name of the bucket being updated
bucketlist_update = api.model('BucketlistUpdate', {
                    'name': fields.String(required=True,
                            description = "The Bucketlist Name Update")
                    })
# This holds names of items being created in a bucket list
items_post_field = api.model('BucketlistItemPost',{
                    'name': fields.String(required=True,
                             description = "Item Name to be added a bucket")})
# This holds name and status(done) of bucket list item to be updated                    })
items_update_field = api.model('BucketlistItemUpdate', {
                    'name': fields.String(
                            description = "Item name to be Edited"),
                    'done': fields.Boolean(
                            description = 'Status of Item True or False')
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
                    'date_created':fields.DateTime,
                    'date_modified': fields.DateTime,
                    'created_by': fields.Integer(
                            description= "User whoc created this bucket")
                    })
bucket_list_items = api.model('BucketListItems', {
                    'id': fields.Integer(description = "Bucket Item ID"),
                    'name': fields.String(
                            description = "Bucketlist Name"),
                    'done': fields.Boolean( description = "True or False"),
                    'date_created':fields.DateTime,
                    'date_modified': fields.DateTime,
                    'created_by': fields.Integer(
                            description= "User who created this bucket")
})

# bucket_list_items_list = api.model(' A list Bucketlist items'),{
#                     ''
# })
# ******** Pagination Section **********
#Set minimum number of items per page
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
    # @cross_origin(origin='*')
    def get(self):
        """ This method returns buckets created by an individual user."""
        args = pagination_arguments.parse_args(request)
        #Set defualt page to be one
        page = args.get('page', 1)
        # Get per_page from query string
        search = args.get('search','')
        per_page = args.get('per_page', 20)

        # Set minimun number of buckets per_page to 20
        if per_page < min_number_of_buckets_per_page:
            per_page = min_number_of_buckets_per_page
        # Set maximum number of items per page to 100
        if per_page > max_number_of_buckets_per_page:
            per_page = max_number_of_buckets_per_page

        if len(search) > 0:
            search = search.lower()
            bucket_lists = Bucketlist.query.filter((Bucketlist.created_by == g.user.id),(func.lower(Bucketlist.name).like("%"+search+"%")))#.paginate(1, 3, False)
        else:
            bucket_lists = Bucketlist.query.filter(Bucketlist.created_by == g.user.id)

        bucket_list_page = bucket_lists.paginate(page, per_page, error_out=False)
        return bucket_list_page

    @api.response(201, 'Success')
    @api.expect(bucketlist_post)
    @auth.login_required
    def post(self):
        """
        This post method is used to create buckets for a user already logged in.
        :params :name
        :returns :200 for succesful post
        """
        args = parser.parse_args()
        name = args.name
        created_by = g.user.id
        try:
            bucket = Bucketlist.query.filter_by(name = name).first()
            if name:
                bucketlist = Bucketlist(name,created_by)
                db.session.add(bucketlist)
                db.session.commit()
                return({'message': 'Bucket list created Successfully'})
        except:
            return {'error_message' : 'Bucket with similar name already exists'}

@api.route('/<bucketlist_id>')
class BucketListView(Resource):
    """This Resource displays, edits and deleted as single bucket"""
    @auth.login_required
    # @api.marshal_with(bucket_list_items)
    def get(self, bucketlist_id):
        """
        This method is used to list details of a bucket and it's items
        :params bucketlist_id: id of individaual bucket to retrieved from the db
        :returns - bucketlist and all it's items
        """
        bucketlist_id = bucketlist_id
        bucket_list_item = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).first()
        single_bucket_list_items = Item.query.filter(Item.bucketlist_id == bucketlist_id).all()
        b_item = ([i.serialize for i in single_bucket_list_items])
        results = {'id': bucket_list_item.id,
                   'name': bucket_list_item.name,
                   'date_created': bucket_list_item.date_created,
                   'date_modified': bucket_list_item.date_modified,
                   'items': b_item
                   }
        return  make_response(jsonify(results))

    @api.response(204, "Update Successful")
    @api.expect(bucketlist_update)
    @auth.login_required
    def put(self, bucketlist_id):
        """
        This method is used to edit/ update the name and status of a bucket
        :params bucketlist_id:
        """
        args = parser.parse_args()
        try:
            update_bucket_list_name = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
            if update_bucket_list_name:
                for bucket in update_bucket_list_name:
                    bucket.name = args.name
                    db.session.add(bucket)
                    db.session.commit()
                    return({'message': 'Bucket list name updated Successfully'})
        except:
            return {"error_message" : "An errro occured while updating bucketname"}

    @auth.login_required
    # @api.doc(params={'bucketlist_id': 'Bucketlist ID'})
    def delete(self, bucketlist_id):
        """
        This method is used to delete buckets and there respective items
        :params bucketlist_id: ID of bucket being deleted
        """
        try:
            # return {"here" : "Hereherererere"}
            delete_bucket_list = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).first()
            # return {"here" : "Hereherererere"}
            if delete_bucket_list:
                db.session.delete(delete_bucket_list)
                db.session.commit()
                return{"message" : "Bucketlist ID deleted succesfully."}

        except Exception as e:
            return {"error_message" : "The Buckelist ID provided doesn't exist ...." + str(e)}


@api.route('/<bucketlist_id>/items')
class BucketListItem(Resource):
    """
    This resource is used to manage creating, updating and deleting items from
    a bucket.
    """
    @api.expect(items_post_field)
    @api.response(200, "Successful")
    @auth.login_required
    def post(self, bucketlist_id):
        """
        This method creates an item in a particular bucket
        :params bucketlist_id: ID of the bucket that we are creating item for
        """
        args = parser.parse_args()
        try:
            get_bucket_list_item = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
            if get_bucket_list_item:
                name = args.name
                done = args.done
                new_item = Item(name, bucketlist_id)
                db.session.add(new_item)
                db.session.commit()
                return({'message': 'Item created Successfully'})
        except:
            return {"error_message": "item already exits"}

@api.route('/<bucketlist_id>/items/<item_id>')
class BucketListItems(Resource):
    @api.expect(items_update_field)
    @auth.login_required
    def put(self, bucketlist_id, item_id):
        """
        This method is used to update the name and status of an item.
        :params bucketlist_id: ID of bucket that contains the item
        :params item_id: ID of the item being updated
        :return : Returns the message item status updated succesfully
        """
        args = parser.parse_args()
        try:
            get_bucket_list_item = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
            if get_bucket_list_item:
                single_bucket_list_item = Item.query.filter(Item.id == item_id).all()
                if single_bucket_list_item:
                    for item in single_bucket_list_item:
                        item.name = args.name
                        item.done = args.done
                        db.session.add(item)
                        db.session.commit()
                        return({'message': 'Item Status updated Successfully'})

        except:
            return {"error_message" : "Bucketlist or item ID is incorrect"}

    @auth.login_required
    def  delete(self, bucketlist_id, item_id):
        """
        This method deletes an item forma bucket list
        :params bucketlist_id: ID of bucketlist the item will be deleted from
        :params item_id: ID of the item being deleted"""
        get_bucket_list_item = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
        if get_bucket_list_item:
            single_bucket_list_item = Item.query.filter(Item.id == item_id).all()
            if single_bucket_list_item:
                for item in single_bucket_list_item:
                    db.session.delete(item)
                    db.session.commit()
