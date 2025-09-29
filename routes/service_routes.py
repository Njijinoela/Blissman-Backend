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
    data = request.json
    service = Service(
        title=data["title"],
        description=data.get("description"),
        image_url=data.get("image_url"),
        icon=data.get("icon"),
        portfolio=data.get("portfolio", []),
        faqs=data.get("faqs", [])
    )
    db.session.add(service)
    db.session.commit()
    return jsonify({"message": "Service added", "id": service.id}), 201

@service_bp.route("/<int:service_id>", methods=["GET"])
def get_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404
    return jsonify(service.to_dict())
