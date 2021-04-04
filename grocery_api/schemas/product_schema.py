from marshmallow import Schema, fields, post_load
from grocery_api.models.product import Product

class ProductSchema(Schema):
    """
    Player Marshmallow Schema
    Marshmallow schema used for loading/dumping Players
    """
    class Meta:
        fields = ('name', 'vendor_id', 'vendor.name')
        
    #vendor.name = fields.String(allow_none=False)
    #position = fields.String(allow_none=False)
    #player_id = fields.Integer()

    #@post_load
    #def make_player(self, data, **kwargs):
    #    return Player(**data)