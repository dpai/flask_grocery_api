from marshmallow import Schema, post_load, validates_schema, ValidationError
from grocery_api.models import shop

class ShopSchema(Schema):
    """
    Shop Marshmallow Schema
    Marshmallow schema used for loading/dumping Shops
    """
    class Meta:
        fields = ('id', 'shop_name', 'location')

    @post_load
    def make_shop(self, data, **kwargs):
        return shop.Shop(**data)

    @validates_schema
    def validate_shop_fields(self, data, **kwargs):
        if (not "shop_name" in data) or (data["shop_name"] in [""]) :
            raise ValidationError({"shop_name": ["Shop Name cannot be empty"]})
        if (not "location" in data) or (data["location"] in [""]) :
            raise ValidationError({"location": ["Location cannot be empty"]})