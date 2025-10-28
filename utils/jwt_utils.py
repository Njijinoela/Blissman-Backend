from flask import request, jsonify
import jwt
import os
from functools import wraps

SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY")

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"success": False, "message": "Missing token"}), 401

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if decoded.get("role") != "admin":
                return jsonify({"success": False, "message": "Forbidden"}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "message": "Invalid token"}), 401

        return f(*args, **kwargs)
    return wrapper
