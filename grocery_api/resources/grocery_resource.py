#import logging

from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from grocery_api.database import db
from grocery_api.models.grocery import Grocery
from grocery_api.schemas.grocery_schema import GrocerySchema


GROCERY_ENDPOINT = "/api/grocery"
#logger = logging.getLogger(__name__)


class GroceryResource(Resource):
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

            return self._get_all_groceries(), 200

        #logger.info(f"Retrieving product by id {id}")

        try:
            return self._get_grocery_by_id(id), 200
        except NoResultFound:
            abort(404, message="Grocery not found")

    def _get_grocery_by_id(self, grocery_id):
        grocery = Grocery.query.filter_by(id=grocery_id).first()
        grocery_json = GrocerySchema().dump(grocery)

        if not grocery_json:
            raise NoResultFound()

        #logger.info(f"Product retrieved from database {product_json}")
        return grocery_json

    def _get_all_groceries(self):
        groceries = Grocery.query.all()

        groceries_json = GrocerySchema(many=True).dump(groceries)

        #logger.info("Players successfully retrieved.")
        return groceries_json

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