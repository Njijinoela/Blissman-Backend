from config import db

class QuoteRequest(db.Model):
    __tablename__ = "quotes"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Foreign keys
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"))

    # Relationships
    customer = db.relationship("User", back_populates="quotes")
    service = db.relationship("Service", back_populates="quotes")
