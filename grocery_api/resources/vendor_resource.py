#import logging

from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from grocery_api.models.vendor import Vendor
from grocery_api.models.product import Product
from grocery_api.schemas.vendor_schema import VendorSchema
from grocery_api.database import db_session


VENDOR_ENDPOINT = "/api/v1/vendors"
#logger = logging.getLogger(__name__)

class VendorByNameResource(Resource):
    def get(self, vendor_name):
        """
        VendorByNameResource GET method. Retrieves the vendor by name if found in the 
        database. If a paramater arugment product_name is provided, will retrieve the 
        vendor only if it makes/holds that product.
        :param vendor_name: Vendor name to retrieve
        :return: Vendor, 200 HTTP status code
        """

        product_name = request.args.get("product_name")

        try:
            vendor_json = self._get_vendor_by_name(vendor_name, product_name)
        except NoResultFound:
            if product_name:
                abort(404, message=f"Vendor {vendor_name} does not have {product_name}")
            else:
                abort(404, message=f"Vendor {vendor_name} not found")
        
        #logger.info(f"Product retrieved from database {vendor_json}")
        return vendor_json, 200

    def _get_vendor_by_name(self, vendor_name, product_name):
        if not product_name:
            vendor = db_session.query(Vendor).filter(Vendor.name==vendor_name).first()
            vendor_json = VendorSchema().dump(vendor)
        else:
            vendor = db_session.query(Vendor).join(Product).filter(Vendor.name == vendor_name).filter(Product.name == product_name).first()
            vendor_json = VendorSchema(exclude=["products"]).dump(vendor)
            vendor_json["product"] = [product_name]

        db_session.remove()

        if not vendor_json:
            raise NoResultFound();

        return vendor_json
class VendorResource(Resource):
    def get(self, id=None):
        """
        VendorResource GET method. Retrieves all vendors found in the database
        or if id is provided retrieve the associated vendor id. 
        :param id: Vendor ID to retrieve, this path parameter is optional
        :return: Product, 200 HTTP status code
        """
        if not id:
            # logger.info(
            #     f"Retrieving all products"
            # )

            return self._get_all_vendors(), 200

        #logger.info(f"Retrieving product by id {id}")

        try:
            return self._get_vendor_by_id(id), 200
        except NoResultFound:
            abort(404, message="Vendor not found")

    def _get_vendor_by_id(self, vendor_id):
        vendor = db_session.query(Vendor).filter_by(id=vendor_id).first()
        vendor_json = VendorSchema().dump(vendor)
        db_session.remove()

        if not vendor_json:
            raise NoResultFound()

        #logger.info(f"Product retrieved from database {product_json}")
        return vendor_json

    def _get_all_vendors(self):
        vendors = db_session.query(Vendor).all()
        vendors_json = VendorSchema(many=True).dump(vendors)
        db_session.remove()

        #logger.info("Vendors successfully retrieved.")
        return vendors_json

    def post(self):
        """
        VendorResource POST method. Adds a new Vendor to the database.
        :return: Vendor.id, 201 HTTP status code.
        """
        vendor = VendorSchema().load(request.get_json())

        try:
            db_session.add(vendor)
            db_session.commit()
        except IntegrityError as e:
            #logger.warning(
            #    f"Integrity Error, this team is already in the database. Error: {e}"
            #)

            abort(500, message="Unexpected Error!")
        else:
            return vendor.id, 201