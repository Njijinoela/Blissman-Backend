from config import db

# Update this to match your actual hosted domain (e.g. your cPanel URL)
BASE_URL = "https://blissman-backend.onrender.com"


class Portfolio(db.Model):
    __tablename__ = "portfolio"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(100), nullable=True)  # e.g. "Wrench"
    
    # relationships
    images = db.relationship("PortfolioImage", backref="portfolio", cascade="all, delete-orphan")
    faqs = db.relationship("PortfolioFAQ", backref="portfolio", cascade="all, delete-orphan")
    media = db.relationship("PortfolioMedia", backref="portfolio", cascade="all, delete-orphan")

    def to_dict(self):
        return {
        "id": self.id,
        "slug": self.slug,
        "title": self.title,
        "description": self.description,
        "icon": self.icon,

        "images": [img.url for img in self.images],

        "videos": [m.url for m in self.media if m.type == "video"],

        "media": [
            {"type": m.type, "url": m.url, "caption": m.caption}
            for m in self.media
        ],

        "faqs": [
            {"question": f.question, "answer": f.answer}
            for f in self.faqs
        ],
    }



class PortfolioImage(db.Model):
    __tablename__ = "portfolio_images"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey("portfolio.id"), nullable=False)


class PortfolioMedia(db.Model):
    __tablename__ = "portfolio_media"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # "image" or "video"
    url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255))
    portfolio_id = db.Column(db.Integer, db.ForeignKey("portfolio.id"), nullable=False)


class PortfolioFAQ(db.Model):
    __tablename__ = "portfolio_faqs"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey("portfolio.id"), nullable=False)
