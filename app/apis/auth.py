from flask_restplus import Namespace, Resource, fields

api = Namespace('auth/mm', description='Authentication Operations')

auth = api.model('User', {
    'id': fields.String(required=True, description='The User identifier'),
    'username': fields.String(required=True,
                              description="The Application User's name"),

})

CATS = [
    {'id': 'felix', 'name': 'Felix'},
]

@api.route('/')
class CatList(Resource):
    @api.doc('list_cats')
    @api.marshal_list_with(auth)
    def get(self):
        '''List all cats'''
        return CATS

@api.route('/<id>')
@api.param('id', 'The cat identifier')
@api.response(404, 'Cat not found')
class Cat(Resource):
    @api.doc('get_cat')
    @api.marshal_with(auth)
    def get(self, id):
        '''Fetch a cat given its identifier'''
        for cat in CATS:
            if cat['id'] == id:
                return cat
        api.abort(404)
