#import logging

from flask_restful import Resource, abort, request
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from grocery_api.models.product import Product
from grocery_api.models.vendor import Vendor
from grocery_api.schemas.product_schema import ProductSchema
from grocery_api.database import db_session

PRODUCT_ENDPOINT = "/api/v1/products"
#logger = logging.getLogger(__name__)

class ProductByNameResource(Resource):
    def get(self, product_name):
        """
        ProductByNameResource GET method. Retrieves the product by name if found in the 
        database. If a paramater arugment vendor_name is provided, will retrieve the 
        product only if the vendor makes it.
        :param product_name: Product name to retrieve
        :return: Product, 200 HTTP status code
        """

        vendor_name = request.args.get("vendor_name")

        try:
            products_json = self._get_product_by_name(product_name, vendor_name)
        except NoResultFound:
            if vendor_name:
                abort(404, message=f"Vendor {vendor_name} does not have {product_name}")
            else:
                abort(404, message=f"Product {product_name} not found")
        
        #logger.info(f"Product retrieved from database {product_json}")
        return products_json, 200

    def _get_product_by_name(self, product_name, vendor_name):
        if not vendor_name:
            products = db_session.query(Product).filter(Product.name==product_name).all()
            products_json = ProductSchema(many=True).dump(products)
        else:
            product = db_session.query(Product).join(Vendor).filter(Product.name==product_name).filter(Vendor.name==vendor_name).first()
            products_json = ProductSchema().dump(product)
        
        db_session.remove()

        if not products_json:
            raise NoResultFound();

        return products_json

class ProductResource(Resource):
    def get(self, id=None):
        """
        ProductResource GET method. Retrieves all products found in the database
        or if id is provided retrieve the associated product id. 
        :param id: Product ID to retrieve, this path parameter is optional
        :return: Product, 200 HTTP status code
        """
        if not id:
            # logger.info(
            #     f"Retrieving all products"
            # )

            return self._get_all_products(), 200

        #logger.info(f"Retrieving product by id {id}")

        try:
            return self._get_product_by_id(id), 200
        except NoResultFound:
            abort(404, message="Product not found")

    def post(self):
        """
        ProductResource POST method. Adds a new Product to the database.
        :return: Product.id, 201 HTTP status code.
        """
        try:
            product = ProductSchema().load(request.get_json())
        except ValidationError as e:
            abort(500, message=e.messages)

        try:
            db_session.add(product)
            db_session.commit()
        except IntegrityError as e:
            # logger.warning(
            #     f"Integrity Error, this team is already in the database. Error: {e}"
            # )

            abort(500, message="Unexpected Error!")
        else:
            return product.id, 201

    def delete(self, id=None):
        """
        ProductResource DELETE method. Delete the product by id if found in the 
        database. 
        :param id: Product id to delete
        :return: Shop, 200 HTTP status code
        """

        if not id:
            abort(405, message="Method not allowed")

        try:
            product_json = self._delete_product_by_id(id)
        except NoResultFound:
            abort(404, message=f"Product not found")
        
        #logger.info(f"Shop deleted from database {shop_json}")
        return product_json, 200

    def _get_product_by_id(self, product_id):
        product = db_session.query(Product).filter_by(id=product_id).first()
        product_json = ProductSchema().dump(product)
        db_session.remove()

        if not product_json:
            raise NoResultFound()

        #logger.info(f"Product retrieved from database {product_json}")
        return product_json

    def _get_all_products(self):
        products = db_session.query(Product).all()
        products_json = ProductSchema(many=True).dump(products)
        db_session.remove()

        #logger.info("Players successfully retrieved.")
        return products_json

    def _delete_product_by_id(self, product_id):
        product = db_session.query(Product).filter(Product.id==product_id).first()
        product_json = ProductSchema().dump(product)

        if not product_json:
            raise NoResultFound()
        
        db_session.delete(product)
        db_session.commit()
        return product_json