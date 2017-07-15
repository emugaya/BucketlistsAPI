from flask_restplus import Namespace, Resource, fields, reqparse

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
parser.add_argument('id')
parser.add_argument('item_id')

@api.route('/')
class BucketLists(Resource):
    """This Resource creates a bucket and lists all buckets"""
    def get(self):
        pass

    @api.param('name','The Bucket list Name')
    @api.marshal_list_with(bucketlist)
    def post(self):
        pass


@api.route('/<id>')
class BucketListView(Resource):
    """This Resource displays, edits and deleted as single bucket"""
    # @api.doc(params={'id': 'Bucket List ID'})
    def get(self, id):
        args = parser.parse_args()
        pass

    # @api.doc(params={'id': 'Bucket List ID'})
    def put(self, id):
        args = parser.parse_args()
        pass

    # @api.doc(params={'id': 'Bucket List ID'})
    def delete(self):
        args = parser.parse_args()
        pass

@api.route('/<id>/items')
class BucketListItem(Resource):
    @api.doc(params={'name':'Item Name','done':'True or False, default False'})
    @api.marshal_list_with(bucketlist_item_fields)
    def post(self,id):
        pass

@api.route('/<id>/items/<item_id>')
class BucketListItems(Resource):
    def put(self, id, item_id):
        args = parser.parse_args()
        pass

    def  delete(self,id, item_id):
        args = parser.parse_args()
        pass
