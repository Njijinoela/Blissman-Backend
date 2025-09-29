from config import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)

    availability = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    specs = db.Column(db.JSON, nullable=True)      
    features = db.Column(db.JSON, nullable=True)   
    warranty = db.Column(db.String(100), nullable=True)

    order_items = db.relationship("OrderItem", back_populates="product")
