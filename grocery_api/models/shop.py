from grocery_api.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref

class Shop(Base):
    __tablename__ = 'shops'
    id = Column(Integer, primary_key=True, autoincrement=True)
    shop_name = Column(String(100))
    location = Column(String(100))
    groceries = relationship('Grocery', backref=backref('shop'))

    def __init__(self, shop_name, location):
        self.shop_name = shop_name
        self.location = location

    def __repr__(self):
        return (
            f"**Shop** "
            f"name: {self.shop_name} "
            f"location: {self.location} "
            f"id: {self.id} "
            f"**Shop** "
        )