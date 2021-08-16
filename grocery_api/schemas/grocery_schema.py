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
        if (not "vendor_id" in data) or (data["vendor_id"] in [""]) :
            raise ValidationError({"vendor_id": ["Vendor field cannot be empty"]})
        if (not "product_id" in data) or (data["product_id"] in [""]) :
            raise ValidationError({"product_id": ["Product field cannot be empty"]})
        if (not "date_bought" in data) or (data["date_bought"] in [""]) :
            raise ValidationError({"date_bought": ["Date Bought field cannot be empty"]})
        if (not "weight_in_pounds" in data) or (data["weight_in_pounds"] in [""]) :
            raise ValidationError({"weight_in_pounds": ["Weight in Pounds field cannot be empty"]})
        if (not "quantity" in data) or (data["quantity"] in [""]) :
            raise ValidationError({"quantity": ["Quantity field cannot be empty"]})
        if (not "price" in data) or (data["price"] in [""]) :
            raise ValidationError({"price": ["Price field cannot be empty"]})