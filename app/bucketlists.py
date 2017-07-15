from flask import Flask, jsonify, make_response
# from flask_restful import reqparse, abort, Api, Resource
from flask_restplus import reqparse, abort, Api, Resource
from sqlalchemy.orm import class_mapper, session, sessionmaker
from json import dumps
from datetime import datetime, date

from bucketlists import app, db, api
from bucketlists.models import BucketList, User, Item

class Helloworld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(Helloworld, '/v1/')

#Get list of all BucketLists and add BucketList
class BucketListView(Resource):
    def get(self):
        bucket_lists = BucketList.query.all()
        return make_response(jsonify([i.serialize for i in bucket_lists]))

    @api.doc(params={'name': 'Bucketlist Name'})
    def post(self):
        name = request.json.get('name')
        new_bucketlist = BucketList(name)
        db.session.add(new_bucketlist)
        db.session.commit()
        return 201

# Add resource for Adding single bucket list and listing all created bucket lists
api.add_resource(BucketListView,'/v1/bucketlists/')

#Display/View/Get, Delete, Update Single BucketList
class BucketListViews(Resource):
    @api.doc(params={'bucket_list_id': 'BucketList ID'})
    def get(self, bucket_list_id):
        args = parser.parse_args()
        bucket_list_item = BucketList.query.filter(BucketList.id == bucket_list_id).all()
        single_bucket_list_items = Item.query.filter(Item.bucketlist_id == bucket_list_id).all()
        b_item = ([i.serialize for i in single_bucket_list_items])
        return  make_response(jsonify([i.serialize_id(b_item) for i in bucket_list_item]))
        # return  ([i.serialize for i in single_bucket_list_items])

    def delete(self, bucket_list_id):
        args = parser.parse_args()
        delete_bucket_list = BucketList.query.filter(BucketList.id == bucket_list_id).all()
        if delete_bucket_list:
            for item in  delete_bucket_list:
                db.session.delete(item)
                db.session.commit()
        return 201

    def put(self, bucket_list_id):
        args = parser.parse_args()
        update_bucket_list_name = BucketList.query.filter(BucketList.id == bucket_list_id).all()
        if update_bucket_list_name:
            for bucket in update_bucket_list_name:
                bucket.name = args.name
                bucket.date_modified = datetime.utcnow()
                db.session.commit()
        return 201

# Add resource for getting, updating, and deleting a single bucket list
api.add_resource(BucketListViews,'/v1/bucketlists/<bucket_list_id>')

#Create a new item in BucketLists

class BucketListItem(Resource):
    def post(self, bucket_list_id):
        args = parser.parse_args()
        get_bucket_list_item = BucketList.query.filter(BucketList.id == bucket_list_id).all()
        if get_bucket_list_item:
            for buckect in get_bucket_list_item:
                new_item = Item(name = args.name, bucketlist_id = bucket_list_id)
                db.session.add(new_item)
                db.session.commit()
        return 201

#Add Resources for creating or adding newbucket list item
api.add_resource(BucketListItem,'/v1/bucketlists/<bucket_list_id>/items/')

# Update and Delete Bucket List item
class BucketListItems(Resource):
    def put(self,bucket_list_id, item_id):
        args = parser.parse_args()
        get_bucket_list_item = BucketList.query.filter(BucketList.id == bucket_list_id).all()
        #print(bucket_list_id)
        if get_bucket_list_item:
            single_bucket_list_items = Item.query.filter(Item.id == item_id).all()
            if single_bucket_list_items:
                for item in single_bucket_list_items:
                    if args.name:
                        item.name = args.name
                        item.date_modified = datetime.utcnow()
                        db.session.commit()
                    if args.done:
                        item.done = args.done
                        print (args.done)
                        item.date_modified = datetime.utcnow()
                        return args.done
                        db.session.commit()

                #772497899

        return 201

    def delete(self, bucket_list_id, item_id):
        args = parser.parse_args()
        get_bucket_list_item = BucketList.query.filter(BucketList.id == bucket_list_id).all()
        if get_bucket_list_item:
            single_bucket_list_items = Item.query.filter(Item.id == item_id).all()
            for item in single_bucket_list_items:
                db.session.delete(item)
                db.session.commit()
        return 201
# Add Resource for updating and deleting bucket list items
api.add_resource(BucketListItems,'/v1/bucketlists/<bucket_list_id>/items/<item_id>')
