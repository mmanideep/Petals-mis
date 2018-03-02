from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt import JWT


app = Flask(__name__)
app.config.from_object('petals_mis.config.DevConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# jwt = JWT(app, authenticate, identity)

from petals_mis.controllers.apis import export_api_list

for api in export_api_list:
    api_url = api.__name__.lower().split("api")[0]
    api_name = api.__name__.lower()
    print api_name, " -> ", "/{}".format(api_url)
    app.add_url_rule(
        "/{}".format(api_url),
        view_func=api.as_view("{}".format(api_name)))
