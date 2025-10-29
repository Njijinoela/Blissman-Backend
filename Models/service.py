from config import db
from sqlalchemy.dialects.postgresql import JSON

# Change this to your actual live site or API base domain:
BASE_URL = "https://blissman-backend.onrender.com"

class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String, nullable=True)
    icon = db.Column(db.String, nullable=True)  # e.g., "Palette"
    portfolio = db.Column(JSON, default=[])     # list of portfolio IDs
    faqs = db.Column(JSON, default=[])          # list of {question, answer}
    
    quotes = db.relationship("QuoteRequest", back_populates="service")

    def to_dict(self):
        """
        Serialize the service model and normalize image URLs.
        Works for both Cloudinary URLs (https://...) and old static paths (/static/...).
        """
        image_url = self.image_url
        if image_url and not image_url.startswith("http"):
            image_url = f"{BASE_URL}/{image_url.lstrip('/')}"

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "image_url": image_url,
            "icon": self.icon,
            "portfolio": self.portfolio,
            "faqs": self.faqs,
        }
