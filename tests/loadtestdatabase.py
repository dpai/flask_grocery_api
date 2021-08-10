
import os
os.environ['DATABASE_URI'] = f"sqlite:///grocery_test.db"
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grocery_api.models import shop, grocery, product, vendor
from grocery_api.database import SessionLocal, engine, Base
from grocery_api.schemas import shop_schema, vendor_schema, product_schema, grocery_schema
import datetime

db = SessionLocal()

Base.metadata.create_all(bind=engine)

## Add 2 shops
shop1 = shop.Shop("Test1", "Wisonsin")
db.add(shop1)
db.commit()

shop2 = shop_schema.ShopSchema().load({"shop_name": "Test2", "location": "Illinois"})
db.add(shop2)
db.commit()

## Add 2 vendors
vendor1 = vendor.Vendor("Vendor1")
db.add(vendor1)
db.commit()

vendor2 = vendor_schema.VendorSchema().load({"name": "Vendor2"})
db.add(vendor2)
db.commit()

## Add 4 products
## Note product.id will not autoincrement in SQlite because of composite primary keys
## So we will add product.id manually. 
product1 = product_schema.ProductSchema().load({"name": "Product1", "vendor_id": "1"})
product1.id = 1
product2 = product_schema.ProductSchema().load({"name": "Product2", "vendor_id": "1"})
product2.id = 2
product3 = product_schema.ProductSchema().load({"name": "Product3", "vendor_id": "1"})
product3.id = 3
product4 = product_schema.ProductSchema().load({"name": "Product4", "vendor_id": "2"})
product4.id = 4
db.add(product1)
db.add(product2)
db.add(product3)
db.add(product4)
db.commit()

## Add groceries
grocery1 = grocery.Grocery(1, 1, 1, 2.99, 1, datetime.datetime(2021, 4, 12), 1)
grocery2 = grocery.Grocery(2, 1, 1, 3.99, 1, datetime.datetime(2021, 1, 6), 1)
grocery3 = grocery.Grocery(1, 4, 2, 4.99, 2, datetime.datetime(2021, 1, 6), 1)
grocery4 = grocery.Grocery(2, 3, 1, 2.99, 2, datetime.datetime(2020, 12, 9), 1)
grocery5 = grocery.Grocery(2, 2, 1, 1.99, 3, datetime.datetime(2020, 12, 9), 2)
grocery6 = grocery.Grocery(1, 2, 1, 5.99, 2, datetime.datetime(2020, 10, 1), 1)
db.add(grocery1)
db.add(grocery2)
db.add(grocery3)
db.add(grocery4)
db.add(grocery5)
db.add(grocery6)
db.commit()

db.close()