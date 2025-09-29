from config import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(50), default="customer")

    # Relationships
    orders = db.relationship("Order", back_populates="customer")
    quotes = db.relationship("QuoteRequest", back_populates="customer")
