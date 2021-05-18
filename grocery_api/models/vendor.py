from grocery_api.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

class Vendor(Base):
    __tablename__ = "vendor"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    products = relationship('Product', backref=backref('vendor'))
    groceries = relationship('Grocery', backref=backref('vendor'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return (
            f"**Vendor** "
            f"name: {self.name} "
            f"id: {self.id}"
            f"**Vendor** "
        )