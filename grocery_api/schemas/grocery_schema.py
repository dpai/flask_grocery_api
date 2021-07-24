from marshmallow import Schema, fields, post_load
from grocery_api.models.grocery import Grocery

class GrocerySchema(Schema):
    """
    Player Marshmallow Schema
    Marshmallow schema used for loading/dumping Players
    """
    class Meta:
        fields = ('id', 'product.name', 'product.vendor.name', 'shop.shop_name', 'price', 'weight_in_pounds', 'date_bought')