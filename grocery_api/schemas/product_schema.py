from marshmallow import Schema, post_load, validates_schema, ValidationError
from grocery_api.models import product
class ProductSchema(Schema):
    """
    Product Marshmallow Schema
    Marshmallow schema used for loading/dumping Products
    """
    class Meta:
        fields = ('id', 'name', 'vendor_id', 'vendor.name')

    @post_load
    def make_product(self, data, **kwargs):
        return product.Product(**data)

    @validates_schema
    def validate_fields(self, data, **kwargs):
        if data["name"] in [""] :
            raise ValidationError({"name": ["Product Name cannot be empty"]})