from flask_restplus import Namespace, Resource, fields, reqparse
from flask import request, jsonify, make_response,g
import json
from app.models import Bucketlist, Item, dump_datetime
from app import db
from sqlalchemy import func, Column, Integer, String
from sqlalchemy.orm import joinedload
from app.routes.auth import auth
from datetime import datetime, date
from flask_cors import CORS, cross_origin

api = Namespace('bucketlists',
                description='Create, Read, Update, Display Buckets and Items')

parser = reqparse.RequestParser()
parser = reqparse.RequestParser()
parser.add_argument('bucketlist_id')
parser.add_argument('item_id')
parser.add_argument('name')
parser.add_argument('item_name')
parser.add_argument('done')
parser.add_argument('user_id')

# This holds names of items being created in a bucket list
items_fields = api.model('BucketlistItemUpdate', {
                    'name': fields.String(
                            description = "Item name to be Edited"),
                    'description': fields.String(description= "Item Description"),
                    'done': fields.Boolean(
                            description = 'Status of Item True or False',
                            default = "false")
                            })

@api.route('/<bucketlist_id>/items/')
class CreateItem(Resource):
    """
    This resource is used to manage creating, updating and deleting items from
    a bucket.
    """
    @api.expect(items_fields)
    @auth.login_required
    def post(self, bucketlist_id):
        """
        This method creates an item in a particular bucket
        :params bucketlist_id: ID of the bucket that we are creating item for
        """
        args = parser.parse_args()
        print("****************")
        print(args)
        print("****************")
        name = args.name
        if not name:
            return {"message": "Please provide a name for your item"}, 400

        bucketlist = Bucketlist.query.filter_by(id = bucketlist_id)
        if not bucketlist:
            return {"message": "Bucketlist Doesn't exist"}, 404

        bucketlist_item = Item.query.filter_by(
            name=name, bucketlist_id=bucketlist_id).first()
        if bucketlist_item:
            return {"message": "Item with this name already exits"}, 400

        name = args.name
        done = args.done
        new_item = Item(name, bucketlist_id)
        db.session.add(new_item)
        db.session.commit()
        return {'message': 'Item created Successfully'}, 201

@api.route('/<bucketlist_id>/items/<item_id>')
class UpdateAndDeleteItem(Resource):
    @api.expect(items_fields)
    @auth.login_required
    def put(self, bucketlist_id, item_id):
        """
        This method is used to update the name and status of an item.
        :params bucketlist_id: ID of bucket that contains the item
        :params item_id: ID of the item being updated
        :return : Returns the message item status updated succesfully
        """
        args = parser.parse_args()
        name = args.name.strip()
        done = args.done.strip()
        if not name:
            return {"message" : "Please Supply Name and done status."}, 400

        if not done:
            return {"message": "Please Supply Name and done status."}, 400
        
        bucketlist = Bucketlist.query.filter(
            Bucketlist.id == bucketlist_id).first()

        if not bucketlist:
            return {"message": "Bucketlist ID " + bucketlist_id + " is incorrect"}, 404
        bucketlist_item = Item.query.filter(Item.id == item_id).first()

        if not bucketlist_item:
            return {"message": "Item " + item_id + "Doesn't Exist"}

        bucketlist_item.name = args.name
        bucketlist_item.done = args.done
        db.session.add(bucketlist_item)
        db.session.commit()
        return {'message': 'Item Status updated Successfully'}, 204

    @auth.login_required
    def  delete(self, bucketlist_id, item_id):
        """
        This method deletes an item from a bucket list
        :params bucketlist_id: ID of bucketlist the item will be deleted from
        :params item_id: ID of the item being deleted"""

        bucketlist = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).first()
        if not bucketlist:
            return {'message': "The Bucket " + bucketlist_id + " passed does not exist"}, 404

        bucketlist_item = Item.query.filter(Item.id == item_id).first()
        if not bucketlist_item:
            return {"message": "Item " + item_id + " Doesn't Exist"}, 404

        db.session.delete(bucketlist_item)
        db.session.commit()
        return {'message':'Item Deleted succesfully'}, 200