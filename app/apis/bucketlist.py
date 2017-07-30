from flask_restplus import Namespace, Resource, fields, reqparse
from flask import request, jsonify, make_response,g
import json
from app.models import Bucketlist, Item
from app import db
from app.apis.auth import auth
from datetime import datetime, date

# This namespace is used to control CRUD operations for buckets and items
api = Namespace('bucketlists',
                description='Create, Read, Update, Display Buckets and Items')

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

@api.route('/')
class BucketLists(Resource):
    """This Resource is used to create buckets and lists all buckets"""
    @api.response(200,'Success')
    @auth.login_required
    def get(self):
        """ This method returns buckets created by an individual user."""
        bucket_lists = Bucketlist.query.filter(Bucketlist.created_by == g.user.id).all()
        return make_response(jsonify([i.serialize for i in bucket_lists]))

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
    def get(self, bucketlist_id):
        """
        This method is used to list details of a bucket and it's items
        :params bucketlist_id: id of individaual bucket to retrieved from the db
        :returns - bucketlist and all it's items
        """
        bucketlist_id = bucketlist_id
        bucket_list_item = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
        single_bucket_list_items = Item.query.filter(Item.bucketlist_id == bucketlist_id).all()
        b_item = ([i.serialize for i in single_bucket_list_items])
        return  make_response(jsonify([i.serialize_id(b_item) for i in bucket_list_item]))

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
    def delete(self, bucketlist_id):
        """
        This method is used to delete buckets and there respective items
        :params bucketlist_id: ID of bucket being deleted
        """
        delete_bucket_list = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
        if delete_bucket_list:
            for item in  delete_bucket_list:
                db.session.delete(item)
                db.session.commit()

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
