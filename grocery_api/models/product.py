from grocery_api.database import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), primary_key=True )
    groceries = db.relationship('Grocery', backref=db.backref('product', lazy=False), lazy=True)

    def __init__(self, name, vendor_id):
        self.name = name
        self.vendor_id = vendor_id

    def __repr__(self):
        return (
            f"**Product** "
            f"name: {self.name} "
            f"vendor_id: {self.vendor_id}"
            f"**Product** "
        )