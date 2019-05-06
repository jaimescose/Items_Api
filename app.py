from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'secret_key'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = [
]

#Resource for Item
class Item(Resource):
    #Create the parser for an Item resource
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field cannot be left blank."
    )

    #Return a specific item given a name
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    #Create a new item given a name
    @jwt_required()
    def post(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)

        if item:
            return {'message': "there is already an item with the given name", 'item': item}, 400
        else:
            data = Item.parser.parse_args()
            item = {'name': name, 'price': data['price']}
            items.append(item)
            return item, 201
    
    #Delete a specific item given a name
    @jwt_required()
    def delete(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            items.remove(item)
            return {'message': "item deleted"}, 200
        else:
            return {'message': "item not found"}, 404

    #Update or create a new item given a name
    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            item.update(data)
            return {'message': "item updated"}, 200
        else:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        return item, 201

    '''
    #(Alternative way for deleting a specific item given a name)
    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': "item deleted", 'items': items}
    '''

#Resource for Items
class ItemList(Resource):
    def get(self):
        return {'items': items}, 200

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

app.run(port=8000, debug=True)