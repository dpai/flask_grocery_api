#import logging

from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from grocery_api.database import db
from grocery_api.models.shop import Shop
from grocery_api.schemas.shop_schema import ShopSchema


SHOP_ENDPOINT = "/api/shop"
#logger = logging.getLogger(__name__)


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
            #     f"Retrieving all products"
            # )

            return self._get_all_shops(), 200

        #logger.info(f"Retrieving product by id {id}")

        try:
            return self._get_shop_by_id(id), 200
        except NoResultFound:
            abort(404, message="Vendor not found")

    def _get_shop_by_id(self, shop_id):
        shop = Shop.query.filter_by(id=shop_id).first()
        shop_json = ShopSchema().dump(product)

        if not shop_json:
            raise NoResultFound()

        #logger.info(f"Product retrieved from database {product_json}")
        return shop_json

    def _get_all_shops(self):
        shops = Shop.query.all()

        shops_json = ShopSchema(many=True).dump(shops)

        #logger.info("Vendors successfully retrieved.")
        return shops_json

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