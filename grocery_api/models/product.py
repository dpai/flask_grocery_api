from grocery_api.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True) ## Ideally need autoincrement=True, but sqlite does not like it.
    name = Column(String(100))
    vendor_id = Column(Integer, ForeignKey('vendor.id'), primary_key=True)
    groceries = relationship('Grocery', backref=backref('product', lazy=False))

    def __init__(self, name, vendor_id, id=None):
        self.name = name
        self.vendor_id = vendor_id
        ## This hack is to enable test with sqlite - Composite primary keys cannot be autoincremented 
        if id is not None:
            self.id = id

    def __repr__(self):
        return (
            f"**Product** "
            f"name: {self.name} "
            f"vendor_id: {self.vendor_id}"
            f"**Product** "
        )