from flask_restplus import Namespace, Resource, fields, reqparse
from flask import request, jsonify, make_response
import json
from app.models import Bucketlist, Item
from app import db
from datetime import datetime, date


api = Namespace('bucketlists',
                description='Create, Read, Update, Display Buckets and Items')


bucketlist_post = api.model('BucketlistPost', {
                    'name': fields.String(required=True,
                            description = "The Bucket List name")
                    })

bucketlist_update = api.model('BucketlistUpdate', {
                    'name': fields.String(required=True,
                            description = "The Bucketlist Name Update")
                    })

items_post_field = api.model('BucketlistItemPost',{
                    'name': fields.String(required=True,
                             description = "Item Name to be added a bucket")
                    })
items_update_field = api.model('BucketlistItemUpdate', {
                    'name': fields.String(
                            description = "Item name to be Edited"),
                    'done': fields.Boolean(
                            description = 'Status of Item True or False')
                    })


parser = reqparse.RequestParser()
parser.add_argument('bucketlist_id')
parser.add_argument('item_id')
parser.add_argument('name')
parser.add_argument('item_name')
parser.add_argument('done')

@api.route('/')
class BucketLists(Resource):
    """This Resource creates a bucket and lists all buckets"""
    @api.response(200,'Success')
    def get(self):
        bucket_lists = Bucketlist.query.all()
        return make_response(jsonify([i.serialize for i in bucket_lists]))

    @api.response(201, 'Success')
    @api.expect(bucketlist_post)
    def post(self):
        args = parser.parse_args()
        name = args.name
        if name:
            bucketlist = Bucketlist(name)
            db.session.add(bucketlist)
            db.session.commit()
            return({'message': 'Bucket list created Successfully'})

@api.route('/<bucketlist_id>')
class BucketListView(Resource):
    """This Resource displays, edits and deleted as single bucket"""
    def get(self, bucketlist_id):
        bucketlist_id = bucketlist_id
        bucket_list_item = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
        single_bucket_list_items = Item.query.filter(Item.bucketlist_id == bucketlist_id).all()
        b_item = ([i.serialize for i in single_bucket_list_items])
        return  make_response(jsonify([i.serialize_id(b_item) for i in bucket_list_item]))

    @api.response(204, "Update Successful")
    @api.expect(bucketlist_update)
    def put(self, bucketlist_id):
        args = parser.parse_args()
        update_bucket_list_name = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
        if update_bucket_list_name:
            for bucket in update_bucket_list_name:
                bucket.name = args.name
                # bucket.date_modified = datetime.utcnow()
                db.session.add(bucket)
                db.session.commit()
                return({'message': 'Bucket list name updated Successfully'})

    def delete(self, bucketlist_id):
        delete_bucket_list = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
        if delete_bucket_list:
            for item in  delete_bucket_list:
                db.session.delete(item)
                db.session.commit()

@api.route('/<bucketlist_id>/items')
class BucketListItem(Resource):
    @api.expect(items_post_field)
    @api.response(200, "Successful")
    def post(self, bucketlist_id):
        args = parser.parse_args()
        get_bucket_list_item = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
        if get_bucket_list_item:
            name = args.item_name
            done = args.done
            new_item = Item(name, bucketlist_id)
            db.session.add(new_item)
            db.session.commit()
            return({'message': 'Item created Successfully'})

@api.route('/<bucketlist_id>/items/<item_id>')
class BucketListItems(Resource):
    @api.expect(items_update_field)
    def put(self, bucketlist_id, item_id):
        args = parser.parse_args()
        get_bucket_list_item = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
        if get_bucket_list_item:
            single_bucket_list_item = Item.query.filter(Item.id == item_id).all()
            if single_bucket_list_item:
                for item in single_bucket_list_item:
                    if args.item_name:
                        item.name = args.item_name
                        # item.date_modified = datetime.utcnow()
                        db.session.add(item)
                        db.session.commit()
                        return({'message': 'Item Name updated Successfully'})
                    if args.done:
                        item.done = args.done
                        # item.date_modified = datetime.utcnow()
                        db.session.add(item)
                        db.session.commit()
                        return({'message': 'Item Status updated Successfully'})

    def  delete(self, bucketlist_id, item_id):
        get_bucket_list_item = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
        if get_bucket_list_item:
            single_bucket_list_item = Item.query.filter(Item.id == item_id).all()
            if single_bucket_list_item:
                for item in single_bucket_list_item:
                    db.session.delete(item)
                    db.session.commit()
