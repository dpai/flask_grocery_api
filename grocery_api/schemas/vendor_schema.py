from marshmallow import Schema, fields, post_load
from grocery_api.models.vendor import Vendor

class VendorSchema(Schema):
    """
    Vendor Marshmallow Schema
    Marshmallow schema used for loading/dumping Vendor
    """
    class Meta:
        additional = ('id', 'name')

    products = fields.Pluck("ProductSchema", "name", many=True)