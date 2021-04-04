from marshmallow import Schema, fields, post_load
from grocery_api.models.grocery import Grocery

class GrocerySchema(Schema):
    """
    Player Marshmallow Schema
    Marshmallow schema used for loading/dumping Players
    """
    class Meta:
        fields = ('product.name', 'vendor.name', 'shop.shop_name', 'price', 'weight_in_pounds', 'date_bought')
        
    #vendor.name = fields.String(allow_none=False)
    #position = fields.String(allow_none=False)
    #player_id = fields.Integer()

    #@post_load
    #def make_player(self, data, **kwargs):
    #    return Player(**data)