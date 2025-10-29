from flask import Blueprint, request, jsonify
from config import db
from Models.service import Service

service_bp = Blueprint("service_bp", __name__, url_prefix="/services")

@service_bp.route("/", methods=["GET"])
def get_services():
    services = Service.query.all()
    return jsonify([s.to_dict() for s in services])


@service_bp.route("/", methods=["POST"])
def add_service():
    data = request.get_json()
    service = Service(
        title=data.get("title"),
        description=data.get("description"),
        image_url=data.get("image_url"),
        icon=data.get("icon"),
        portfolio=data.get("portfolio", []),
        faqs=data.get("faqs", [])
    )
    db.session.add(service)
    db.session.commit()
    return jsonify(service.to_dict()), 201

@service_bp.route("/<int:service_id>", methods=["GET", "PUT", "DELETE"])
def handle_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    if request.method == "GET":
        return jsonify(service.to_dict())

    elif request.method == "PUT":
        data = request.get_json()
        service.title = data.get("title", service.title)
        service.description = data.get("description", service.description)
        service.image_url = data.get("image_url", service.image_url)
        service.icon = data.get("icon", service.icon)
        service.portfolio = data.get("portfolio", service.portfolio)
        service.faqs = data.get("faqs", service.faqs)
        db.session.commit()
        return jsonify(service.to_dict())

    elif request.method == "DELETE":
        db.session.delete(service)
        db.session.commit()
        return jsonify({"message": "Service deleted"}), 200
