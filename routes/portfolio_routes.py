from flask import Blueprint, request, jsonify
from config import db
from Models.portfolio import Portfolio, PortfolioImage, PortfolioMedia, PortfolioFAQ

portfolio_bp = Blueprint("portfolio_bp", __name__, url_prefix="/portfolio")


@portfolio_bp.route("/", methods=["GET"])
def get_portfolios():
    try:
        portfolios = Portfolio.query.all()
        return jsonify([p.to_dict() for p in portfolios]), 200
    except Exception as e:
        print("❌ Error in get_portfolios:", e)
        return jsonify({"error": str(e)}), 500


@portfolio_bp.route("/<string:slug_or_id>", methods=["GET"])
def get_portfolio_detail(slug_or_id):
    try:
        # Check if it's an integer ID or a slug
        if slug_or_id.isdigit():
            portfolio = Portfolio.query.get(int(slug_or_id))
        else:
            portfolio = Portfolio.query.filter_by(slug=slug_or_id).first()

        if not portfolio:
            return jsonify({"error": "Portfolio not found"}), 404

        return jsonify(portfolio.to_dict()), 200

    except Exception as e:
        print("❌ Error in get_portfolio_detail:", e)
        return jsonify({"error": str(e)}), 500


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

@portfolio_bp.route("/", methods=["POST"])
def create_portfolio():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    icon = data.get("icon")
    slug = data.get("slug")

    portfolio = Portfolio(title=title, description=description, icon=icon, slug=slug)
    db.session.add(portfolio)
    db.session.commit()

    # ✅ Handle images
    images = data.get("images", [])
    for img in images:
        if "url" in img:
            db.session.add(PortfolioImage(url=img["url"], portfolio_id=portfolio.id))

    # ✅ Handle media (optional, if you support videos)
    media_items = data.get("media", [])
    for m in media_items:
        if "url" in m:
            db.session.add(PortfolioMedia(url=m["url"], portfolio_id=portfolio.id))

    db.session.commit()

    return jsonify({
        "message": "Portfolio created successfully",
        "id": portfolio.id
    }), 201


@portfolio_bp.route("/<int:portfolio_id>", methods=["PUT"])
def update_portfolio(portfolio_id):
    data = request.get_json()
    portfolio = Portfolio.query.get_or_404(portfolio_id)

    portfolio.title = data.get("title", portfolio.title)
    portfolio.description = data.get("description", portfolio.description)
    portfolio.icon = data.get("icon", portfolio.icon)
    portfolio.slug = data.get("slug", portfolio.slug)
    db.session.commit()

    # ✅ Refresh portfolio images (simple replace)
    PortfolioImage.query.filter_by(portfolio_id=portfolio.id).delete()
    images = data.get("images", [])
    for img in images:
        if "url" in img:
            db.session.add(PortfolioImage(url=img["url"], portfolio_id=portfolio.id))

    db.session.commit()

    return jsonify({"message": "Portfolio updated successfully"}), 200

@portfolio_bp.route("/<int:portfolio_id>", methods=["DELETE"])
def delete_portfolio(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    db.session.delete(portfolio)
    db.session.commit()
    return jsonify({"message": "Portfolio deleted successfully"}), 200
