from grocery_api.database import db

class Shop(db.Model):
    __tablename__ = 'shops'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shop_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    groceries = db.relationship('Grocery', backref=db.backref('shop'))

    def __init__(self, name, location):
        self.shop_name = name
        self.location = location

    def __repr__(self):
        return (
            f"**Shop** "
            f"name: {self.shop_name} "
            f"location: {self.location} "
            f"id: {self.id} "
            f"**Shop** "
        )