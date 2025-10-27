from flask import Blueprint, request, jsonify
from config import db
from Models.portfolio import Portfolio, PortfolioImage, PortfolioMedia, PortfolioFAQ

portfolio_bp = Blueprint("portfolio_bp", __name__, url_prefix="/portfolio")

@portfolio_bp.route("/", methods=["GET"])
def get_portfolio():
    portfolios = Portfolio.query.all()
    return jsonify([
        {
            "id": p.id,
            "slug": p.slug,
            "title": p.title,
            "description": p.description,
            "icon": p.icon,
            "images": [img.url for img in p.images],
            "media": [
                {"type": m.type, "url": m.url, "caption": m.caption} for m in p.media
            ],
            "faqs": [
                {"question": f.question, "answer": f.answer} for f in p.faqs
            ]
        } for p in portfolios
    ])


@portfolio_bp.route("/<string:slug>", methods=["GET"])
def get_portfolio_item(slug):
    p = Portfolio.query.filter_by(slug=slug).first_or_404()
    return jsonify({
        "id": p.id,
        "slug": p.slug,
        "title": p.title,
        "description": p.description,
        "icon": p.icon,
        "images": [img.url for img in p.images],
        "media": [
            {"type": m.type, "url": m.url, "caption": m.caption} for m in p.media
        ],
        "faqs": [
            {"question": f.question, "answer": f.answer} for f in p.faqs
        ]
    })

@portfolio_bp.route("/<int:portfolio_id>/faqs", methods=["POST"])
def add_portfolio_faq(portfolio_id):
    data = request.get_json()
    question = data.get("question")
    answer = data.get("answer")

    if not question or not answer:
        return jsonify({"error": "Question and answer are required"}), 400

    faq = PortfolioFAQ(question=question, answer=answer, portfolio_id=portfolio_id)
    db.session.add(faq)
    db.session.commit()

    return jsonify({
        "message": "FAQ added successfully",
        "faq": {"id": faq.id, "question": faq.question, "answer": faq.answer}
    }), 201


@portfolio_bp.route("/faqs/<int:faq_id>", methods=["DELETE"])
def delete_portfolio_faq(faq_id):
    faq = PortfolioFAQ.query.get_or_404(faq_id)
    db.session.delete(faq)
    db.session.commit()
    return jsonify({"message": "FAQ deleted successfully"}), 200

@portfolio_bp.route("/faqs/<int:faq_id>", methods=["PUT"])
def update_faq(faq_id):
    faq = PortfolioFAQ.query.get_or_404(faq_id)
    data = request.get_json()
    faq.question = data.get("question", faq.question)
    faq.answer = data.get("answer", faq.answer)
    db.session.commit()
    return jsonify({"message": "FAQ updated", "faq": {"id": faq.id, "question": faq.question, "answer": faq.answer}})
