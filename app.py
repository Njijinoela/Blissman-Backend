from config import create_app, db
from Models import *
from routes.product_routes import product_bp
from routes.order_routes import order_bp
from routes.service_routes import service_bp
from routes.portfolio_routes import portfolio_bp
from routes.team_routes import team_bp
from routes.quote_routes import quote_bp
from routes.contact_routes import contact_bp
from routes.auth_routes import auth_bp
from flask_migrate import Migrate
from flask_cors import CORS
from flask import request, jsonify
import os
from werkzeug.utils import secure_filename


app = create_app() 

CORS(app, resources={
    r"/*": {
        "origins": [
            "https://blissman.ke",
            "https://www.blissman.ke",
            "http://localhost:5173",
        ]
    }
}, supports_credentials=True,
methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"])

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response



migrate = Migrate(app, db)



app.register_blueprint(product_bp)
app.register_blueprint(order_bp)
app.register_blueprint(service_bp)
app.register_blueprint(portfolio_bp)
app.register_blueprint(team_bp)
app.register_blueprint(quote_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(auth_bp)



@app.route("/")
def home():
    return "Flask + Supabase connected with Flask-Migrate!"


UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Construct full accessible URL
    base_url = request.host_url.rstrip("/")
    file_url = f"{base_url}/{filepath}"

    return jsonify({"url": file_url})