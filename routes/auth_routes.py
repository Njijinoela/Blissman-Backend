from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from Models.user import User
import jwt
import datetime
import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

auth_bp = Blueprint("auth_bp", __name__)

# Load secret key from .env or fallback
SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY")


@auth_bp.route("/admin/login", methods=["POST", "OPTIONS"])
def admin_login():
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.get_json() or {}
    username_or_email = data.get("username")
    password = data.get("password")

    if not username_or_email or not password:
        return jsonify({"success": False, "message": "Missing credentials"}), 400

    try:
        # Check if User table exists and query safely
        user = User.query.filter(
            or_
            (User.email == username_or_email,
             User.name == username_or_email)
        ).first()

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 401

        if user.role != "admin":
            return jsonify({"success": False, "message": "Not authorized"}), 403

        if not user.password_hash:
            return jsonify({"success": False, "message": "Password not set for user"}), 401


        if not check_password_hash(user.password_hash, password):
            return jsonify({"success": False, "message": "Incorrect password"}), 401
        
        # Generate JWT token
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

    except SQLAlchemyError as e:
        # Catch database errors
        print("Database error:", str(e))
        return jsonify({"success": False, "message": "Database error"}), 500

    except Exception as e:
        # Catch all other errors
        print("Unexpected error:", str(e))
        return jsonify({"success": False, "message": "Internal server error"}), 500
