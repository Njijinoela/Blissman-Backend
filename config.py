from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy import text
import os
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def create_app():
    app = Flask(__name__)

    load_dotenv()

    # Try full DATABASE_URL first (Render/Supabase often provides this)
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        # Otherwise, build from individual vars
        DB_NAME = os.getenv("DB_NAME")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT", 5432)

        if not all([DB_NAME, DB_USER, DB_PASSWORD, DB_HOST]):
            raise ValueError("Missing one or more database configuration environment variables.")

        database_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    #  Always append SSL requirement safely
    if "?sslmode=" not in database_url:
        database_url += "?sslmode=require"

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Optional: test DB connection
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
            print("✅ Database connection successful")
        except Exception as e:
            print("❌ Database connection failed:", e)

    return app
