from flask_jwt import jwt_required

from petals_mis.controllers.base import CrudResource
from petals_mis.models.models import User, InventoryItem, ProductInventory, Product, PurchaseLog, SellLog
from petals_mis.settings import ADMIN, USER, MANAGER


class UserAPI(CrudResource):
    _model = User
    _private_attrs = ["password", "created_at", "updated_at"]
    _restrict_updates = ["email_address", "username", "password"]
    _allowed_methods = ["GET", "POST", "PUT"]
    decorators = [jwt_required()]
    priority = {"GET": MANAGER, "POST": ADMIN, "PUT": ADMIN}


class InventoryAPI(CrudResource):
    login_required = True
    _model = InventoryItem
    decorators = [jwt_required()]
    priority = {"GET": USER, "POST": MANAGER, "DELETE": MANAGER, "PUT": MANAGER}


class ProductInventoryAPI(CrudResource):
    _model = ProductInventory
    login_required = True
    decorators = [jwt_required()]
    priority = {"GET": USER, "POST": MANAGER, "DELETE": MANAGER, "PUT": MANAGER}


class ProductAPI(CrudResource):
    _model = Product
    login_required = True
    decorators = [jwt_required()]
    priority = {"GET": USER, "POST": MANAGER, "DELETE": MANAGER, "PUT": MANAGER}


class PurchaseLogAPI(CrudResource):
    _model = PurchaseLog
    login_required = True
    decorators = [jwt_required()]
    priority = {"GET": USER, "POST": MANAGER, "DELETE": MANAGER, "PUT": MANAGER}


class SellLogAPI(CrudResource):
    _model = SellLog
    login_required = True
    decorators = [jwt_required()]
    priority = {"GET": USER, "POST": MANAGER, "DELETE": MANAGER, "PUT": MANAGER}


export_api_list = [UserAPI, InventoryAPI, ProductInventoryAPI, ProductAPI, PurchaseLogAPI, SellLogAPI]
