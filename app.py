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
import cloudinary
import cloudinary.uploader


app = create_app() 

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

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


migrate = Migrate(app, db)



app.register_blueprint(product_bp)
app.register_blueprint(order_bp)
app.register_blueprint(service_bp)
app.register_blueprint(portfolio_bp)
app.register_blueprint(team_bp)
app.register_blueprint(quote_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(auth_bp)



@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    try:
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file,
            folder="blissman_uploads",  # optional folder name
            resource_type="auto"  # handles both images & videos
        )

        # Cloudinary returns a permanent URL
        return jsonify({
            "url": upload_result["secure_url"],
            "public_id": upload_result["public_id"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500