from marshmallow import Schema, fields, post_load, validates_schema, ValidationError
from grocery_api.models import grocery

class GrocerySchema(Schema):
    """
    Player Marshmallow Schema
    Marshmallow schema used for loading/dumping Players
    """
    class Meta:
        fields = ('id', 'product_id', 'product.name', 'vendor_id', 'product.vendor.name', 'shop_id', 'shop.shop_name', 'price', 'weight_in_pounds', 'date_bought', 'quantity')

    @post_load
    def make_product(self, data, **kwargs):
        return grocery.Grocery(**data)

    @validates_schema
    def validate_fields(self, data, **kwargs):
        if (not "shop_id" in data) or (data["shop_id"] in [""]) :
            raise ValidationError({"shop_id": ["Shop field cannot be empty"]})