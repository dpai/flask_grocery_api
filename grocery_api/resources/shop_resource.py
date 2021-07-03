#import logging

from flask_restful import Resource, abort, request
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from grocery_api.models.shop import Shop
from grocery_api.schemas.shop_schema import ShopSchema
from grocery_api.database import db_session

SHOP_ENDPOINT = "/api/v1/shops"
#logger = logging.getLogger(__name__)

class ShopByNameResource(Resource):
    def get(self, shop_name):
        """
        ShopByNameResource GET method. Retrieves the shop by name if found in the 
        database. 
        :param shop_name: Shop name to retrieve
        :return: Shop, 200 HTTP status code
        """

        try:
            shop_json = self._get_shop_by_name(shop_name)
        except NoResultFound:
            abort(404, message=f"{shop_name} not found")
        
        #logger.info(f"Shop retrieved from database {shop_json}")
        return shop_json, 200

    def delete(self, shop_name):
        """
        ShopByNameResource DELETE method. Delete the shop by name if found in the 
        database. 
        :param shop_name: Shop name to delete
        :return: Shop, 200 HTTP status code
        """

        try:
            shop_json = self._delete_shop_by_name(shop_name)
        except NoResultFound:
            abort(404, message=f"{shop_name} not found")
        
        #logger.info(f"Shop deleted from database {shop_json}")
        return shop_json, 200

    def _delete_shop_by_name(self, shop_name):
        shop = db_session.query(Shop).filter(Shop.shop_name==shop_name).first()
        shop_json = ShopSchema().dump(shop)

        if not shop_json:
            raise NoResultFound()
        
        db_session.delete(shop)
        db_session.commit()
        return shop_json

    def _get_shop_by_name(self, shop_name):
        shop = db_session.query(Shop).filter(Shop.shop_name==shop_name).first()
        shop_json = ShopSchema().dump(shop)

        db_session.remove()

        if not shop_json:
            raise NoResultFound()

        return shop_json
class ShopResource(Resource):
    def get(self, id=None):
        """
        ShopResource GET method. Retrieves all shops found in the database
        or if id is provided retrieve the associated shop id. 
        :param id: Shop ID to retrieve, this path parameter is optional
        :return: Shop, 200 HTTP status code
        """
        if not id:
            # logger.info(
            #     f"Retrieving all shops"
            # )

            return self._get_all_shops(), 200

        #logger.info(f"Retrieving shop by id {id}")

        try:
            return self._get_shop_by_id(id), 200
        except NoResultFound:
            abort(404, message="Shop not found")

    def delete(self, id=None):
        """
        ShopByNameResource DELETE method. Delete the shop by id if found in the 
        database. 
        :param id: Shop id to delete
        :return: Shop, 200 HTTP status code
        """

        if not id:
            abort(405, message="Method not allowed")

        try:
            shop_json = self._delete_shop_by_id(id)
        except NoResultFound:
            abort(404, message=f"Shop not found")
        
        #logger.info(f"Shop deleted from database {shop_json}")
        return shop_json, 200

    def post(self):
        """
        ShopResource POST method. Adds a new Shop to the database.
        :return: Shop.id, 201 HTTP status code.
        """
        try:
            shop = ShopSchema().load(request.get_json())
        except ValidationError as e:
            abort(500, message=e.messages)

        try:
            db_session.add(shop)
            db_session.commit()
        except IntegrityError as e:
            # logger.warning(
            #     f"Integrity Error, this team is already in the database. Error: {e}"
            # )

            abort(500, message="Unexpected Error!")
        else:
            return shop.id, 201

    def put(self, id=None):
        """
        ShopResource PUT method. Updates Shop to the database.
        :return: Shop.id, 201 HTTP status code.
        """

        if not id:
            abort(405, message="Method not allowed")

        data = request.get_json()

        try:
            shop = ShopSchema().load(data)
        except ValidationError as e:
            abort(500, message=e.messages)
        
        shop = db_session.query(Shop).filter(Shop.id==id).first()

        shop.shop_name = data["shop_name"]
        shop.location = data["location"]

        try:
            db_session.commit()
        except IntegrityError as e:
            # logger.warning(
            #     f"Integrity Error, this team is already in the database. Error: {e}"
            # )

            abort(500, message="Unexpected Error!")
        else:
            return shop.id, 200


    def _delete_shop_by_id(self, shop_id):
        shop = db_session.query(Shop).filter(Shop.id==shop_id).first()
        shop_json = ShopSchema().dump(shop)

        if not shop_json:
            raise NoResultFound()
        
        db_session.delete(shop)
        db_session.commit()
        return shop_json

    def _get_shop_by_id(self, shop_id):
        shop = db_session.query(Shop).filter_by(id=shop_id).first()
        shop_json = ShopSchema().dump(shop)
        db_session.remove()

        if not shop_json:
            raise NoResultFound()

        #logger.info(f"Shop retrieved from database {shop_json}")
        return shop_json

    def _get_all_shops(self):
        shops = db_session.query(Shop).all()
        shops_json = ShopSchema(many=True).dump(shops)
        db_session.remove()

        #logger.info("Shops successfully retrieved.")
        return shops_json