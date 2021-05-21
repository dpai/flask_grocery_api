from marshmallow import Schema

class ShopSchema(Schema):
    """
    Shop Marshmallow Schema
    Marshmallow schema used for loading/dumping Shops
    """
    class Meta:
        fields = ('id', 'shop_name', 'location')