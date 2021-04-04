from marshmallow import Schema, fields, post_load
from grocery_api.models.shop import Shop

class ShopSchema(Schema):
    """
    Player Marshmallow Schema
    Marshmallow schema used for loading/dumping Shops
    """
    class Meta:
        fields = ('shop_name', 'location')
        
    #name = fields.String(allow_none=False)
    #position = fields.String(allow_none=False)
    #player_id = fields.Integer()

    #@post_load
    #def make_player(self, data, **kwargs):
    #    return Player(**data)