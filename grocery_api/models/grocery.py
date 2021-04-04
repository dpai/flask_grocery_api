from grocery_api.database import db

class Grocery(db.Model):
    __tablename__ = "groceries"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    price = db.Column(db.Float)
    weight_in_pounds = db.Column(db.Float)
    date_bought = db.Column(db.Date())
    quantity = db.Column(db.Integer)

    def __init__(self, shop_id, product_id, vendor_id, price, weight_in_pounds, quantity):
        self.shop_id = shop_id
        self.product_id = product_id
        self.vendor_id = vendor_id
        self.price = price
        self.weight_in_pounds = weight_in_pounds
        self.quantity = quantity

    def __repr__(self):
        return (
            f"**Grocery** "
            f"name: {self.product_id} "
            f"product.name: {self.product.name}"
            f"vendor.name: {self.vendor.name}"
            f"shop.name: {self.shop.name}"
            f"price: {self.price}"
            f"weight_in_pounds: {self.weight_in_pounds}"
            f"**Grocery** "
        )