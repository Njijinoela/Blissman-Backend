from config import db
from sqlalchemy.dialects.postgresql import JSON

class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)  
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String, nullable=True)
    icon = db.Column(db.String, nullable=True)  # store icon name, e.g., "Palette"
    portfolio = db.Column(JSON, default=[])     # list of portfolio IDs
    faqs = db.Column(JSON, default=[]) 
             # list of {question, answer}
    quotes = db.relationship("QuoteRequest", back_populates="service")
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "image_url": self.image_url,
            "icon": self.icon,
            "portfolio": self.portfolio,
            "faqs": self.faqs,
        }
