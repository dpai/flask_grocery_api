from datetime import date
from sqlalchemy.sql.expression import null
from grocery_api.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, ForeignKeyConstraint
from sqlalchemy.types import Date
from sqlalchemy.orm import relationship
import datetime

class Grocery(Base):
    __tablename__ = "groceries"
    __table_args__ = (
        ForeignKeyConstraint(['product_id', 'vendor_id'], ['product.id', 'product.vendor_id'], name='fk_productvendor'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    shop_id = Column(Integer, ForeignKey('shops.id'), nullable=False)
    product_id = Column(Integer, nullable=False)
    vendor_id = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    weight_in_pounds = Column(Float, nullable=False)
    date_bought = Column(Date(), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    def __init__(self, shop_id, product_id, vendor_id, price, weight_in_pounds, date_bought, quantity):
        self.shop_id = shop_id
        self.product_id = product_id
        self.vendor_id = vendor_id
        self.price = price
        self.weight_in_pounds = weight_in_pounds
        self.date_bought = datetime.datetime.fromisoformat(date_bought)
        self.quantity = quantity

    def __repr__(self):
        return (
            f"**Grocery** "
            f"id: {self.product_id} "
            f"product.name: {self.product.name}"
            f"vendor.name: {self.vendor.name}"
            f"shop.name: {self.shop.name}"
            f"price: {self.price}"
            f"weight_in_pounds: {self.weight_in_pounds}"
            f"date_bought: {self.date_bought}"
            f"quantity: {self.quantity}"
            f"**Grocery** "
        )