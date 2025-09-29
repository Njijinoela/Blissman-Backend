from flask import Blueprint, request, jsonify
from config import db
from Models.team import TeamMember

team_bp = Blueprint("team_bp", __name__, url_prefix="/team")

@team_bp.route("/", methods=["GET"])
def get_team():
    members = TeamMember.query.all()
    return jsonify([
        {"id": m.id, "name": m.name, "role": m.role, "bio": m.bio, "image_url": m.image_url}
        for m in members
    ])

@team_bp.route("/", methods=["POST"])
def add_team_member():
    data = request.json
    member = TeamMember(
        name=data["name"],
        role=data["role"],
        bio=data.get("bio"),
        image_url=data.get("image_url")
    )
    db.session.add(member)
    db.session.commit()
    return jsonify({"message": "Team member added", "id": member.id}), 201
