from flask_restplus import Namespace, Resource, fields, reqparse
from flask import request, jsonify, make_response
import json
from app.models import Bucketlist, Item
from app import db
from datetime import datetime, date


api = Namespace('bucketlists',
                description='Create, Read, Update, Display Buckets and Items')

bucketlist = api.model('BucketList', {
             'id':fields.Integer(description = 'Bucket list id'),
             'name': fields.String(required=True,
                    description = "The Bucket List name"),
             'date_created' : fields.DateTime(dt_format='rfc822',
                    descrpiton ='The Date a Bucketlist was created'),
             'date_modified' : fields.DateTime(dt_format='rfc822',
                    descrpiton = 'The Date a Bucketlist was modified')
             })

bucketlist_post_field = api.model('Resource', {'name': fields.String})

bucketlist_item_fields = api.model('BucketListItem',{
            'id': fields.Integer(description = 'Item ID'),
            'name': fields.String(description= 'Item Name'),
            'date_created':fields.String(dt_format='rfc822',
                                  description = 'Date Item was created') ,
            'date_modified' : fields.String(dt_format='rfc822',
                                  descrpiton = 'Date Item was modified'),
            'done': fields.Boolean(description = 'Status of Item, Completed or Not.')
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
        # print(request)
        bucket_lists = Bucketlist.query.all()
        return make_response(jsonify([i.serialize for i in bucket_lists]))

    @api.doc(params ={'name': "Bucket Name"})
    @api.response(201, 'Success')
    def post(self):
        # print(request)
        args = parser.parse_args()
        name = args.name
        if name:
            bucketlist = Bucketlist(name)
            db.session.add(bucketlist)
            db.session.commit()

@api.route('/<bucketlist_id>')
class BucketListView(Resource):
    """This Resource displays, edits and deleted as single bucket"""
    # @api.doc(params={'bucketlist_id': 'Bucket List ID'})
    def get(self, bucketlist_id):
        bucketlist_id = bucketlist_id
        bucket_list_item = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
        single_bucket_list_items = Item.query.filter(Item.bucketlist_id == bucketlist_id).all()
        b_item = ([i.serialize for i in single_bucket_list_items])
        return  make_response(jsonify([i.serialize_id(b_item) for i in bucket_list_item]))
        # return {"hello":"world"}

    # @api.doc(params={'id': 'Bucket List ID'})
    @api.response(204, "Update Successful")
    @api.doc(params ={'name': "Bucket Name"})
    def put(self, bucketlist_id):
        args = parser.parse_args()
        update_bucket_list_name = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
        if update_bucket_list_name:
            for bucket in update_bucket_list_name:
                bucket.name = args.name
                bucket.date_modified = datetime.utcnow()
                db.session.add(bucket)
                db.session.commit()


    def delete(self, bucketlist_id):
        delete_bucket_list = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
        if delete_bucket_list:
            for item in  delete_bucket_list:
                db.session.delete(item)
                db.session.commit()

@api.route('/<bucketlist_id>/items')
class BucketListItem(Resource):
    @api.doc(params ={'item_name': "Item Name"})
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

@api.route('/<bucketlist_id>/items/<item_id>')
class BucketListItems(Resource):
    def put(self, bucketlist_id, item_id):
        args = parser.parse_args()
        get_bucket_list_item = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
        if get_bucket_list_item:
            single_bucket_list_item = Item.query.filter(Item.id == item_id).all()
            if single_bucket_list_item:
                for item in single_bucket_list_item:
                    if args.item_name:
                        item.name = args.item_name
                        item.date_modified = datetime.utcnow()
                        db.session.add(item)
                        db.session.commit()
                    if args.done:
                        item.done = args.done
                        item.date_modified = datetime.utcnow()
                        db.session.add(item)
                        db.session.commit()

    def  delete(self, bucketlist_id, item_id):
        get_bucket_list_item = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
        if get_bucket_list_item:
            single_bucket_list_item = Item.query.filter(Item.id == item_id).all()
            if single_bucket_list_item:
                for item in single_bucket_list_item:
                    db.session.delete(item)
                    db.session.commit()
