from grocery_api.database import db

class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    products = db.relationship('Product', backref=db.backref('vendor'))
    groceries = db.relationship('Grocery', backref=db.backref('vendor'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return (
            f"**Vendor** "
            f"name: {self.name} "
            f"id: {self.id}"
            f"**Vendor** "
        )