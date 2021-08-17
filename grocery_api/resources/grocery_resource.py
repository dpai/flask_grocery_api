#import logging

from flask_restful import Resource, abort, request
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from grocery_api.database import db_session
from grocery_api.models.grocery import Grocery
from grocery_api.models.product import Product
from grocery_api.models.vendor import Vendor
from grocery_api.schemas.grocery_schema import GrocerySchema


GROCERY_ENDPOINT = "/api/v1/groceries"
#logger = logging.getLogger(__name__)

class GroceryByProductNameResource(Resource):
    def get(self, product_name):
        """
        GroceryByProductNameResource GET method. Retrieves the grocery by product name if found in the 
        database. If a paramater arugment vendor_name is provided, will filter the grocery by that name
        :param product_name: Grocery to retrieve with name product_name
        :return: Grocery, 200 HTTP status code
        """
        vendor_name = request.args.get("vendor_name")

        try:
            grocerys_json = self._filter_grocery_by_vendor(product_name, vendor_name)
        except NoResultFound:
            if vendor_name:
                abort(404, message=f"Vendor {vendor_name} does not have {product_name}")
            else:
                abort(404, message=f"Product {product_name} not found")

        #logger.info(f"Product retrieved from database {product_json}")
        return grocerys_json, 200

    def _filter_grocery_by_vendor(self, product_name, vendor_name):
        if vendor_name:
            grocery = db_session.query(Grocery).join(Product).join(Vendor).filter(Product.name == product_name).filter(Vendor.name==vendor_name).order_by(Grocery.shop_id).all()
            grocerys_json = GrocerySchema(exclude=['id'], many=True).dump(grocery)
        else:
            grocery = db_session.query(Grocery).join(Product).filter(Product.name == product_name).order_by(Grocery.shop_id).all()
            grocerys_json = GrocerySchema(exclude=['id'], many=True).dump(grocery)

        db_session.remove()

        if not grocerys_json:
            raise NoResultFound()

        return grocerys_json
class GroceryResource(Resource):
    def get(self, id=None):
        """
        GroceryResource GET method. Retrieves all grocerys found in the database
        or if id is provided retrieve the associated grocery id. 
        :param id: Grocery ID to retrieve, this path parameter is optional
        :return: Grocery, 200 HTTP status code
        """
        if not id:
            # logger.info(
            #     f"Retrieving all products"
            # )

            return self._get_all_groceries(), 200

        #logger.info(f"Retrieving product by id {id}")

        try:
            return self._get_grocery_by_id(id), 200
        except NoResultFound:
            abort(404, message="Grocery not found")

    def post(self):
        """
        GroceryResource POST method. Adds a new grocery to the database.
        :return: Grocery.idid, 201 HTTP status code.
        """
        try:
            grocery = GrocerySchema().load(request.get_json())
        except ValidationError as e:
            abort(500, message=e.messages)

        try:
            db_session.add(grocery)
            db_session.commit()
        except IntegrityError as e:
            # logger.warning(
            #     f"Integrity Error, this grocery is already in the database. Error: {e}"
            # )

            abort(500, message="Unexpected Error!")
        else:
            return grocery.id, 201

    def delete(self, id=None):
        """
        GroceryResource DELETE method. Delete the grocery by id if found in the 
        database. 
        :param id: Grocery id to delete
        :return: Shop, 200 HTTP status code
        """

        if not id:
            abort(405, message="Method not allowed")

        try:
            grocery_json = self._delete_grocery_by_id(id)
        except NoResultFound:
            abort(404, message=f"Grocery not found")
        
        #logger.info(f"Shop deleted from database {shop_json}")
        return grocery_json, 200

    def _get_grocery_by_id(self, grocery_id):
        grocery = db_session.query(Grocery).filter_by(id=grocery_id).first()
        grocery_json = GrocerySchema(exclude=['id', 'shop_id', 'product_id', 'vendor_id']).dump(grocery)
        db_session.remove()

        if not grocery_json:
            raise NoResultFound()

        #logger.info(f"Product retrieved from database {product_json}")
        return grocery_json

    def _get_all_groceries(self):
        groceries = db_session.query(Grocery).all()
        groceries_json = GrocerySchema(many=True).dump(groceries)
        db_session.remove()

        #logger.info("Players successfully retrieved.")
        return groceries_json

    def _delete_grocery_by_id(self, grocery_id):
        grocery = db_session.query(Grocery).filter(Grocery.id==grocery_id).first()
        grocery_json = GrocerySchema().dump(grocery)

        if not grocery_json:
            raise NoResultFound()
        
        db_session.delete(grocery)
        db_session.commit()
        return grocery_json