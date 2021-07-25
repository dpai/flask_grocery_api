from grocery_api.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

class Vendor(Base):
    __tablename__ = "vendor"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    ### https://docs.sqlalchemy.org/en/14/orm/cascades.html#passive-deletes - The passive_delete property is needed because we 
    ### need to propagate the error from the database (Foreign Key constraint violated in this case), and if this is set to default 
    ### False, the child foreign key on product.vendor_id will be nulled out giving an AssertionError. Setting to "all" will disable
    ### nulling out and propagate the database error up as expected.
    products = relationship('Product', backref=backref('vendor'), passive_deletes="all")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return (
            f"**Vendor** "
            f"name: {self.name} "
            f"id: {self.id}"
            f"**Vendor** "
        )