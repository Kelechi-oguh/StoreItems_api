from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}


class Item(Resource):

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "An error occured while getting item"}, 500
        if item:
            return item.json(), 200
        return {"message": "Item not found"}, 404
        
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "Item with name {} alredy exists".format(name)}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("price", type=float, required=True, help="This field cannot be left blank")
        parser.add_argument("store_id", type=int, required=True, help="Every item needs a store ID")

        data = parser.parse_args()
        item = ItemModel(name, data["price"], data["store_id"])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured while inserting item"}, 500
        return item.json(), 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("name", default=name, ignore=False)
        parser.add_argument("price", type=float, required=True, help="This field must not be left blank")
        
        item = ItemModel.find_by_name(name)
        
        if item is None:
            parser.add_argument("store_id", type=int, required=True, help="Every item needs a store ID")
            data = parser.parse_args()
            try:
                item = ItemModel(name, data["price"], data["store_id"])
            except:
                return {"message": "An error occured while inserting item"}, 500          
        else:
            parser.add_argument("store_id", type=int, default=item.store_id, help="Every item needs a store ID")
            data = parser.parse_args()
            try:
                item.name = data["name"]
                item.price = data["price"]
                item.store_id = data["store_id"]
            except:
                return {"message": "An error occured while updating item"}, 500
        
        item.save_to_db()
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {"message": "Item does not exist"}, 404

        item.delete_from_db()
        return {"message": "Item, {} deleted".format(name)}, 200
