
import os
os.environ['DATABASE_URI'] = f"sqlite:///grocery_test.db"
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grocery_api.models import shop, grocery, product, vendor
from grocery_api.database import SessionLocal, engine, Base
from grocery_api.schemas import shop_schema, vendor_schema, product_schema

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


db.close()