from flask import Blueprint, request, jsonify
from config import db
from Models.contact import ContactMessage

contact_bp = Blueprint("contact_bp", __name__, url_prefix="/contact")

@contact_bp.route("/", methods=["GET"])
def get_messages():
    messages = ContactMessage.query.all()
    return jsonify([
        {"id": m.id, "name": m.name, "email": m.email, "message": m.message}
        for m in messages
    ])

@contact_bp.route("/", methods=["POST"])
def add_message():
    data = request.json
    msg = ContactMessage(
        name=data["name"],
        email=data["email"],
        message=data["message"]
    )
    db.session.add(msg)
    db.session.commit()
    return jsonify({"message": "Message added", "id": msg.id}), 201
