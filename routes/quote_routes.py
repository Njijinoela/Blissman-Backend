from flask import Blueprint, request, jsonify
from config import db
from Models.quote import QuoteRequest

quote_bp = Blueprint("quote_bp", __name__, url_prefix="/quotes")

@quote_bp.route("/", methods=["GET"])
def get_quotes():
    quotes = QuoteRequest.query.all()
    return jsonify([
        {"id": q.id, "message": q.message, "customer_id": q.customer_id, "service_id": q.service_id}
        for q in quotes
    ])

@quote_bp.route("/", methods=["POST"])
def add_quote():
    data = request.json
    quote = QuoteRequest(
        message=data.get("message"),
        customer_id=data["customer_id"],
        service_id=data["service_id"]
    )
    db.session.add(quote)
    db.session.commit()
    return jsonify({"message": "Quote request added", "id": quote.id}), 201
