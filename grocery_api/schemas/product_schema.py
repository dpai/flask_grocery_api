from marshmallow import Schema
class ProductSchema(Schema):
    """
    Product Marshmallow Schema
    Marshmallow schema used for loading/dumping Products
    """
    class Meta:
        fields = ('name', 'vendor_id', 'vendor.name')