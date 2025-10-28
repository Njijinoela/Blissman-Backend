from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from Models import User
from config import db
import jwt
import datetime
import os
from utils.jwt_utils import admin_required

auth_bp = Blueprint("auth_bp", __name__)

# Load secret key from .env or use default fallback
SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY")

@auth_bp.route("/admin/login", methods=["POST", "OPTIONS"])
@admin_required
def admin_login():
    data = request.get_json()
    username_or_email = data.get("username")
    password = data.get("password")

    if not username_or_email or not password:
        return jsonify({"success": False, "message": "Missing credentials"}), 400

    user = User.query.filter(
        (User.email == username_or_email) | (User.name == username_or_email)
    ).first()

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 401

    if user.role != "admin":
        return jsonify({"success": False, "message": "Not authorized"}), 403

    if not check_password_hash(user.password_hash, password):
        return jsonify({"success": False, "message": "Incorrect password"}), 401

    # ✅ Generate JWT token
    token = jwt.encode(
        {
            "user_id": user.id,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "success": True,
        "message": "Admin login successful",
        "token": token,
        "admin_name": user.name
    }), 200
