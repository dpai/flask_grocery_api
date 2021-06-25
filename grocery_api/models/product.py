from grocery_api.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    vendor_id = Column(Integer, ForeignKey('vendor.id'), primary_key=True )
    groceries = relationship('Grocery', backref=backref('product', lazy=False))

    def __init__(self, name, vendor_id):
        self.name = name
        self.vendor_id = vendor_id

    def __repr__(self):
        return (
            f"**Product** "
            f"name: {self.name} "
            f"vendor_id: {self.vendor_id}"
            f"**Product** "
        )