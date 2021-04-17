#import logging

from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from grocery_api.database import db
from grocery_api.models.product import Product
from grocery_api.schemas.product_schema import ProductSchema

PRODUCT_ENDPOINT = "/api/product"
#logger = logging.getLogger(__name__)


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

    def _get_product_by_id(self, product_id):
        product = Product.query.filter_by(id=product_id).first()
        product_json = ProductSchema().dump(product)

        if not product_json:
            raise NoResultFound()

        #logger.info(f"Product retrieved from database {product_json}")
        return product_json

    def _get_all_products(self):
        products = Product.query.all()

        #products_json = [ProductSchema().dump(product) for product in products]
        products_json = ProductSchema(many=True).dump(products)

        #logger.info("Players successfully retrieved.")
        return products_json

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