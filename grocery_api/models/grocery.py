from grocery_api.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.types import Date
from sqlalchemy.orm import relationship

class Grocery(Base):
    __tablename__ = "groceries"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    shop_id = Column(Integer, ForeignKey('shops.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    vendor_id = Column(Integer, ForeignKey('vendor.id'))
    price = Column(Float)
    weight_in_pounds = Column(Float)
    date_bought = Column(Date())
    quantity = Column(Integer)

    def __init__(self, shop_id, product_id, vendor_id, price, weight_in_pounds, quantity):
        self.shop_id = shop_id
        self.product_id = product_id
        self.vendor_id = vendor_id
        self.price = price
        self.weight_in_pounds = weight_in_pounds
        self.quantity = quantity

    def __repr__(self):
        return (
            f"**Grocery** "
            f"name: {self.product_id} "
            f"product.name: {self.product.name}"
            f"vendor.name: {self.vendor.name}"
            f"shop.name: {self.shop.name}"
            f"price: {self.price}"
            f"weight_in_pounds: {self.weight_in_pounds}"
            f"**Grocery** "
        )