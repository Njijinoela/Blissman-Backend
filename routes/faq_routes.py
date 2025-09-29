from flask import Blueprint, request, jsonify
from config import db
from Models.faq import FAQ

faq_bp = Blueprint("faq_bp", __name__, url_prefix="/faq")

@faq_bp.route("/", methods=["GET"])
def get_faqs():
    faqs = FAQ.query.all()
    return jsonify([
        {"id": f.id, "question": f.question, "answer": f.answer}
        for f in faqs
    ])

@faq_bp.route("/", methods=["POST"])
def add_faq():
    data = request.json
    faq = FAQ(
        question=data["question"],
        answer=data["answer"]
    )
    db.session.add(faq)
    db.session.commit()
    return jsonify({"message": "FAQ added", "id": faq.id}), 201
