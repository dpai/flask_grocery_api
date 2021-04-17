import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from flask import Flask
from flask_restful import Api
from grocery_api.constants import PROJECT_ROOT
from database import db, GROCERY_DATABASE
from grocery_api.models.product import Product
from grocery_api.models.vendor import Vendor
from grocery_api.models.shop import Shop
from grocery_api.models.grocery import Grocery
from grocery_api.schemas.product_schema import ProductSchema
from grocery_api.schemas.vendor_schema import VendorSchema
from grocery_api.schemas.shop_schema import ShopSchema
from grocery_api.schemas.grocery_schema import GrocerySchema
from grocery_api.resources.product_resource import ProductResource, PRODUCT_ENDPOINT
from grocery_api.resources.vendor_resource import VendorResource, VENDOR_ENDPOINT
from grocery_api.resources.shop_resource import ShopResource, SHOP_ENDPOINT
from grocery_api.resources.grocery_resource import GroceryResource, GroceryByProductNameResource, GROCERY_ENDPOINT

def create_app(db_location):
    # Init app
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = db_location
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #Init db
    db.init_app(app)

    api = Api(app)

    api.add_resource(ProductResource, PRODUCT_ENDPOINT, f"{PRODUCT_ENDPOINT}/<id>")
    api.add_resource(VendorResource, VENDOR_ENDPOINT, f"{VENDOR_ENDPOINT}/<id>")
    api.add_resource(ShopResource, SHOP_ENDPOINT, f"{SHOP_ENDPOINT}/<id>")
    api.add_resource(GroceryResource, GROCERY_ENDPOINT, f"{GROCERY_ENDPOINT}/<int:id>")
    api.add_resource(GroceryByProductNameResource, GROCERY_ENDPOINT, f"{GROCERY_ENDPOINT}/<string:name>")

    return app

#Init schema
# product_schema = ProductSchema()
# products_schema = ProductSchema(many=True)

# # Get ALl products
# @app.route('/product', methods=['GET'])
# def get_products():
#     all_products = Product.query.all()
#     result = products_schema.dump(all_products)
#     return jsonify(result)

# Run server
if __name__ == '__main__':
    app = create_app(GROCERY_DATABASE)
    app.run(debug=True)