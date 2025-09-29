# seed_portfolio.py
from config import create_app, db
from Models.portfolio import Portfolio, PortfolioImage, PortfolioMedia, PortfolioFAQ

app = create_app()
app.app_context().push()

# 🚨 Clear old data first (only during dev!)
db.session.query(PortfolioFAQ).delete()
db.session.query(PortfolioMedia).delete()
db.session.query(PortfolioImage).delete()
db.session.query(Portfolio).delete()
db.session.commit()

# ===================== SEED DATA =====================
portfolio_items = [
    {
        "slug": "repairs",
        "title": "Repair of Computers & Printers",
        "description": "We diagnose hardware & software faults, remove malware & viruses, replace screens & much more.",
        "icon": "Wrench",
        "images": ["/services/rcp1.jpeg", "/services/rcp2.jpeg"],
        "media": [],
        "faqs": [
            {"question": "How long does a typical repair take?", "answer": "Most repairs are completed within 1–3 business days depending on parts availability."},
            {"question": "Do you use original spare parts?", "answer": "Yes, we prioritize using genuine spare parts to ensure durability and performance."},
        ],
    },
    {
        "slug": "maintenance",
        "title": "Preventative Maintenance",
        "description": "Monthly checks to prolong computer & printer life, improve performance, and ensure reliability.",
        "icon": "ShieldCheck",
        "images": ["/services/pm.jpeg"],
        "media": [],
        "faqs": [
            {"question": "How often should maintenance be done?", "answer": "We recommend monthly or quarterly maintenance for optimal performance and longevity."},
        ],
    },
    {
        "slug": "networking",
        "title": "Structured Networking Solutions",
        "description": "We design, sell, install, and support networks for SMEs & enterprises, plus cable management.",
        "icon": "Network",
        "images": ["/services/sns1.jpeg"],
        "media": [
            {"type": "image", "url": "/projects/starlinkinstallation.jpeg", "caption": "Mounted Starlink Project."},
            {"type": "video", "url": "/projects/starlinkvideo.mp4", "caption": "Installation process by our team."},
        ],
        "faqs": [
            {"question": "Do you handle both wired and wireless networks?", "answer": "Yes, we install and support both wired LAN and wireless Wi-Fi networks."},
        ],
    },
    {
        "slug": "products",
        "title": "ICT Equipment Supply",
        "description": "Supply of computers, laptops, printers, networking devices, and accessories at competitive prices.",
        "icon": "Package",
        "images": ["/services/ict.jpeg"],
        "media": [],
        "faqs": [
            {"question": "Do you provide warranties?", "answer": "Yes, all supplied products come with manufacturer or supplier warranties."},
        ],
    },
    {
        "slug": "security",
        "title": "CCTV Installation & Access Control",
        "description": "Professional installation of CCTV cameras, biometric systems, and access control for enhanced security.",
        "icon": "Camera",
        "images": ["/services/cctv.jpeg"],
        "media": [],
        "faqs": [
            {"question": "Can I monitor cameras remotely?", "answer": "Yes, we configure remote monitoring so you can view live feeds via mobile or PC."},
        ],
    },
    {
        "slug": "software",
        "title": "Software Development & Deployment",
        "description": "Custom software, ERPs, CRMs, and web apps tailored to your business needs.",
        "icon": "Code",
        "images": ["/services/software.jpeg"],
        "media": [],
        "faqs": [
            {"question": "Do you also maintain the software?", "answer": "Yes, we provide ongoing support, updates, and feature improvements."},
        ],
    },
    {
        "slug": "printing",
        "title": "Graphic Design & Printing Services",
        "description": "Design and printing of business cards, flyers, banners, branding materials, and more.",
        "icon": "Printer",
        "images": ["/services/printing.jpeg"],
        "media": [],
        "faqs": [
            {"question": "Do you handle bulk printing orders?", "answer": "Yes, we can handle both small and large-scale printing jobs efficiently."},
        ],
    },
]

# ===================== INSERT INTO DB =====================
for item in portfolio_items:
    portfolio = Portfolio(
        slug=item["slug"],
        title=item["title"],
        description=item["description"],
        icon=item["icon"],
    )
    db.session.add(portfolio)
    db.session.flush()  # 🔑 fetch portfolio.id before adding children

    # Add images
    for img in item.get("images", []):
        db.session.add(PortfolioImage(url=img, portfolio_id=portfolio.id))

    # Add media
    for m in item.get("media", []):
        db.session.add(PortfolioMedia(
            type=m["type"],
            url=m["url"],
            caption=m.get("caption"),
            portfolio_id=portfolio.id
        ))

    # Add FAQs
    for f in item.get("faqs", []):
        db.session.add(PortfolioFAQ(
            question=f["question"],
            answer=f["answer"],
            portfolio_id=portfolio.id
        ))

db.session.commit()
print("✅ Portfolio data seeded successfully!")
