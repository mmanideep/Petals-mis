from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt import JWT


app = Flask(__name__)
app.config.from_object('petals_mis.config.DevConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# jwt = JWT(app, authenticate, identity)

from petals_mis.controllers.apis import UserAPI, InventoryAPI

app.add_url_rule("/user", view_func=UserAPI.as_view("users"))
app.add_url_rule("/inventory-item", view_func=InventoryAPI.as_view("inventory"))
