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
