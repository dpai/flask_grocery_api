from marshmallow import Schema, fields, post_load
from grocery_api.models.vendor import Vendor

class VendorSchema(Schema):
    """
    Player Marshmallow Schema
    Marshmallow schema used for loading/dumping Players
    """
    class Meta:
        additional = ('id', 'name')

    #products = fields.List(fields.Nested("ProductSchema", only=("name",)))
    products = fields.Pluck("ProductSchema", "name", many=True)

    #@post_load
    #def make_vendor(self, data, **kwargs):
    #    return Vendor(**data)