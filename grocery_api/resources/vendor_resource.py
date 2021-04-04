#import logging

from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from grocery_api.database import db
from grocery_api.models.vendor import Vendor
from grocery_api.schemas.vendor_schema import VendorSchema


VENDOR_ENDPOINT = "/api/vendor"
#logger = logging.getLogger(__name__)


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
        vendor = Vendor.query.filter_by(id=vendor_id).first()
        vendor_json = VendorSchema().dump(vendor)

        if not vendor_json:
            raise NoResultFound()

        #logger.info(f"Product retrieved from database {product_json}")
        return vendor_json

    def _get_all_vendors(self):
        vendors = Vendor.query.all()

        vendors_json = VendorSchema(many=True).dump(vendors)

        #logger.info("Vendors successfully retrieved.")
        return vendors_json

    # def post(self):
    #     """
    #     PlayersResource POST method. Adds a new Player to the database.
    #     :return: Player.player_id, 201 HTTP status code.
    #     """
    #     player = PlayerSchema().load(request.get_json())

    #     try:
    #         db.session.add(player)
    #         db.session.commit()
    #     except IntegrityError as e:
    #         logger.warning(
    #             f"Integrity Error, this team is already in the database. Error: {e}"
    #         )

    #         abort(500, message="Unexpected Error!")
    #     else:
    #         return player.player_id, 201