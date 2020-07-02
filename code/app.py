import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authentication, identity
from resources.user import UserRegister
from resources.item import ItemList, Item
from resources.store import StoreList, Store
from db import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "AgdkwwbgnlsvbB"

api = Api(app)

jwt = JWT(app, authentication, identity)  # JWT creates a new endpoint called /auth

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(StoreList, "/stores")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(UserRegister, "/register")

db.init_app(app)
if __name__ == "__main__":
    app.run(debug=True)