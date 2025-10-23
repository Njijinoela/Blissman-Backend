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

    # Try DATABASE_URL first (Render/Supabase full URI)
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        # Fallback for local development
        DB_NAME = os.getenv("DB_NAME")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT", 5432)

        if not all([DB_NAME, DB_USER, DB_PASSWORD, DB_HOST]):
            raise ValueError("Missing one or more database configuration environment variables.")

        database_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Optional test: confirm DB connection on startup
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
            print("✅ Database connection successful")
        except Exception as e:
            print("❌ Database connection failed:", e)

    return app
