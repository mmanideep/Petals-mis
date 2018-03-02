from petals_mis.controllers.base import CrudResource
from petals_mis.models.models import User, InventoryItem, ProductInventory, Product, PurchaseLog, SellLog


class UserAPI(CrudResource):
    _model = User
    _private_attrs = ["password", "created_at", "updated_at"]
    _restrict_updates = ["email_address", "username", "password"]
    _allowed_methods = ["GET", "POST", "PUT"]


class InventoryAPI(CrudResource):
    _model = InventoryItem


class ProductInventoryAPI(CrudResource):
    _model = ProductInventory


class ProductAPI(CrudResource):
    _model = Product


class PurchaseLogAPI(CrudResource):
    _model = PurchaseLog


class SellLogAPI(CrudResource):
    _model = SellLog


export_api_list = [UserAPI, InventoryAPI, ProductInventoryAPI, ProductAPI, PurchaseLogAPI, SellLogAPI]
