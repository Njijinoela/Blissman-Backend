from config import db

BASE_URL = "https://blissman-backend.onrender.com"  # <-- change this to your actual domain

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

    def to_dict(self):
        """
        Serialize the product model and normalize image URL for frontend display.
        Handles both legacy static paths and Cloudinary URLs.
        """
        image_url = self.image_url
        if image_url and not image_url.startswith("http"):
            image_url = f"{BASE_URL}/{image_url.lstrip('/')}"

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),  # Convert Decimal → float
            "image_url": image_url,
            "availability": self.availability,
            "category": self.category,
            "specs": self.specs,
            "features": self.features,
            "warranty": self.warranty,
        }
