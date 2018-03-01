from petals_mis.controllers.base import CrudResource
from petals_mis.models.models import *


class UserAPI(CrudResource):
    _model = User
    _private_attrs = ["password", "created_at", "updated_at"]


class InventoryAPI(CrudResource):
    _model = InventoryItem
