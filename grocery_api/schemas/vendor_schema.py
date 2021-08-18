from marshmallow import Schema, fields, post_load, validates_schema, ValidationError
from grocery_api.models.vendor import Vendor

class VendorSchema(Schema):
    """
    Vendor Marshmallow Schema
    Marshmallow schema used for loading/dumping Vendor
    """
    class Meta:
        additional = ('id', 'name')

    products = fields.Pluck("ProductSchema", "name", many=True)

    @post_load
    def make_vendor(self, data, **kwargs):
        return Vendor(**data)

    @validates_schema
    def validate_vendor_name(self, data, **kwargs):
        if (not "name" in data) or (data["name"] in [""]) :
            raise ValidationError({"name": ["Vendor Name cannot be empty"]})