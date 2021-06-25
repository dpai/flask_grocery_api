import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from flask import Flask
from flask_restful import Api
from grocery_api.database import db_session
from grocery_api.resources.product_resource import ProductResource, ProductByNameResource, PRODUCT_ENDPOINT
from grocery_api.resources.vendor_resource import VendorResource, VendorByNameResource, VENDOR_ENDPOINT
from grocery_api.resources.shop_resource import ShopResource, ShopByNameResource, SHOP_ENDPOINT
from grocery_api.resources.grocery_resource import GroceryResource, GroceryByProductNameResource, GROCERY_ENDPOINT

def create_app(config_object=None):
    # Init app
    app = Flask(__name__)
    app.config.from_object(config_object)

    api = Api(app)

    api.add_resource(ProductResource, PRODUCT_ENDPOINT, f"{PRODUCT_ENDPOINT}/<int:id>")
    api.add_resource(ProductByNameResource, PRODUCT_ENDPOINT, f"{PRODUCT_ENDPOINT}/<string:product_name>")
    api.add_resource(VendorResource, VENDOR_ENDPOINT, f"{VENDOR_ENDPOINT}/<int:id>")
    api.add_resource(VendorByNameResource, VENDOR_ENDPOINT, f"{VENDOR_ENDPOINT}/<string:vendor_name>")
    api.add_resource(ShopResource, SHOP_ENDPOINT, f"{SHOP_ENDPOINT}/<int:id>")
    api.add_resource(ShopByNameResource, SHOP_ENDPOINT, f"{SHOP_ENDPOINT}/<string:shop_name>")
    api.add_resource(GroceryResource, GROCERY_ENDPOINT, f"{GROCERY_ENDPOINT}/<int:id>")
    api.add_resource(GroceryByProductNameResource, GROCERY_ENDPOINT, f"{GROCERY_ENDPOINT}/<string:product_name>")

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app