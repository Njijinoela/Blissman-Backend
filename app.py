from config import create_app, db
from Models import *
from routes.product_routes import product_bp
from routes.order_routes import order_bp
from routes.service_routes import service_bp
from routes.portfolio_routes import portfolio_bp
from routes.team_routes import team_bp
from routes.quote_routes import quote_bp
from routes.contact_routes import contact_bp
from routes.faq_routes import faq_bp
from flask_migrate import Migrate
from flask_cors import CORS


app = create_app() 

CORS(app, resources={r"/*": {"origins": "*"}})

migrate = Migrate(app, db)



app.register_blueprint(product_bp)
app.register_blueprint(order_bp)
app.register_blueprint(service_bp)
app.register_blueprint(portfolio_bp)
app.register_blueprint(team_bp)
app.register_blueprint(quote_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(faq_bp)


@app.route("/")
def home():
    return "Flask + Supabase connected with Flask-Migrate!"
