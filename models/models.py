import uuid
import hashlib
import re

from petals_mis.app import db
from petals_mis.models.custom_types import ChoiceType


def key_gen():
    return uuid.uuid4().hex


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(32), primary_key=True, default=key_gen)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.current_timestamp())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)


class InventoryItem(BaseModel):
    __tablename__ = "inventory_item"

    TYPES = [
        ("flower", "Flower"),
        ("packing-item", "Packing Item"),
        ("other", "Other")
    ]

    type = db.Column(ChoiceType(TYPES))
    name = db.Column(db.String(32))
    count = db.Column(db.Float, default=0.0)


class Product(BaseModel):
    __tablename__ = "product"

    TYPES = [
        ("bouquet", "Bouquet"),
        ("flower", "Flower")
    ]
    name = db.Column(db.String(32))
    cost = db.Column(db.Float)
    type = db.Column(ChoiceType(TYPES))


class ProductInventory(BaseModel):
    __tablename__ = "product_inventory"

    product_id = db.Column(db.String, db.ForeignKey('product.id'))
    inventory_id = db.Column(db.String, db.ForeignKey('inventory_item.id'))
    quantity = db.Column(db.Float)


class PurchaseLog(BaseModel):
    __tablename__ = "purchase_log"

    inventory_id = db.Column(db.String, db.ForeignKey('product.id'))
    quantity = db.Column(db.Float)
    total_cost = db.Column(db.Float)

    def save(self):
        inv_obj = db.session.query(InventoryItem).filter(self.inventory_id == InventoryItem.id).first()
        inv_obj.count += self.quantity
        try:
            db.session.add(inv_obj)
            db.session.add(self)
            return db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def destroy(self):
        try:
            inv_obj = db.session.query(InventoryItem).filter(self.inventory_id == InventoryItem.id).first()
            inv_obj.count -= self.quantity
            db.session.add(inv_obj)
            db.session.delete(self)
            return db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)


class SellLog(BaseModel):
    __tablename__ = "sell_log"

    product_id = db.Column(db.String, db.ForeignKey('product.id'))
    quantity = db.Column(db.Float)

    def save(self):
        # Write raw sql query to optimize
        try:
            prod_inventories = db.session.query(ProductInventory).filter(
                ProductInventory.product_id == self.product_id).all()
            for prod_inv in prod_inventories:
                inv_obj = db.session.query(InventoryItem).filter(
                    InventoryItem.id == prod_inv.inventory_id).first()
                inv_obj.count -= prod_inv.quantity
                db.session.add(inv_obj)
            db.session.add(self)
            return db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def destroy(self):
        try:
            prod_inventories = db.session.query(ProductInventory).filter(
                ProductInventory.product_id == self.product_id).all()
            for prod_inv in prod_inventories:
                inv_obj = db.session.query(InventoryItem).filter(
                    InventoryItem.id == prod_inv.inventory_id).first()
                inv_obj.count += prod_inv.quantity
                db.session.add(inv_obj)
            db.session.delete(self)
            return db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)


class User(BaseModel):
    __tablename__ = "user"

    username = db.Column(db.String(32))
    first_name = db.Column(db.String(32), nullable=True)
    last_name = db.Column(db.String(32), nullable=True)
    email_address = db.Column(db.String(64))
    password = db.Column(db.String(32))
    priority = db.Column(db.Integer)

    def save(self):
        self.password = hashlib.md5(self.password).hexdigest()
        email_regex = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
        if not re.match(email_regex, self.email_address):
            raise Exception("Enter valid email address")
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)
