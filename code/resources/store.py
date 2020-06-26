from flask_restful import Resource
from models.store import StoreModel

class StoreList(Resource):
    def get(self):
        return {"Stores": [store.json() for store in StoreModel.query.all()]}

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {"message": "Store does not exist"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "Store with name {} already exists".format(name)}, 400
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occured while creating store"}
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": "Store '{}' deleted".format(name)}