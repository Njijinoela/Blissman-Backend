from app import create_app, db
from Models.product import Product

PRODUCTS = [
    {
        "id": 1,
        "name": "HP EliteBook 840 G7",
        "description": "Business-class laptop with Intel i7, 16GB RAM, and 512GB SSD.",
        "price": 49500,
        "availability": "In Stock",
        "category": "Laptops",
        "image_url": "/products/hpelite.jpeg",
        "specs": {
            "processor": "Intel Core i7 10th Gen",
            "memory": "16GB DDR4 RAM",
            "storage": "512GB SSD",
            "display": "14-inch FHD (1920x1080)",
            "os": "Windows 11 Pro",
        },
        "features": [
            "Slim and lightweight design",
            "Long-lasting battery (up to 12 hours)",
            "Backlit keyboard",
            "Fingerprint reader",
        ],
        "warranty": "1 Year Manufacturer Warranty",
    },
    {
        "id": 2,
        "name": "Canon LaserJet Printer",
        "description": "High-speed wireless printer, perfect for office environments.",
        "price": 33200,
        "availability": "Out of Stock",
        "category": "Printers",
        "image_url": "/products/canon.jpeg",
        "specs": {
            "type": "Laser Printer",
            "connectivity": "WiFi, USB, Ethernet",
            "printSpeed": "38 ppm",
            "resolution": "1200 x 1200 dpi",
        },
        "features": [
            "Wireless printing from mobile devices",
            "Automatic double-sided printing",
            "Energy-efficient mode",
        ],
        "warranty": "6 Months Warranty",
    },
    {
        "id": 3,
        "name": "CCTV Camera Kit (4 Cameras + DVR)",
        "description": "Complete security surveillance kit with night vision.",
        "price": 14500,
        "availability": "In Stock",
        "category": "Security",
        "image_url": "/products/cctv.jpeg",
        "specs": {
            "cameras": "4 HD 1080p Cameras",
            "dvr": "4-Channel DVR",
            "storage": "Supports up to 2TB HDD",
            "nightVision": "Up to 30m",
        },
        "features": [
            "Mobile remote viewing",
            "Motion detection alerts",
            "Weatherproof outdoor cameras",
        ],
        "warranty": "1 Year Warranty",
    },
    {
        "id": 4,
        "name": "Lenovo ThinkCentre Desktop",
        "description": "Powerful desktop for businesses with Intel i5 and 8GB RAM.",
        "price": 87000,
        "availability": "Limited Stock",
        "category": "Desktops",
        "image_url": "/products/lenovothinkcenter.jpeg",
        "specs": {
            "processor": "Intel Core i5 9th Gen",
            "memory": "8GB DDR4 RAM",
            "storage": "1TB HDD + 256GB SSD",
            "os": "Windows 11 Pro",
        },
        "features": [
            "Compact business design",
            "Multiple USB & HDMI ports",
            "Energy efficient",
        ],
        "warranty": "1 Year Warranty",
    },
    {
        "id": 5,
        "name": "TP-Link WiFi 6 Router",
        "description": "High-performance router with dual-band WiFi 6 technology.",
        "price": 3180,
        "availability": "In Stock",
        "category": "Networking",
        "image_url": "/products/tp-link.webp",
        "specs": {
            "wifiStandard": "WiFi 6 (802.11ax)",
            "speed": "Up to 1.8Gbps",
            "bands": "Dual-Band 2.4GHz & 5GHz",
            "ports": "4 Gigabit LAN, 1 Gigabit WAN",
        },
        "features": [
            "MU-MIMO technology",
            "Improved coverage with beamforming",
            "Easy app setup & control",
        ],
        "warranty": "2 Year Warranty",
    },
]

app = create_app()

with app.app_context():
    for data in PRODUCTS:
        product = Product.query.get(data["id"])
        if not product:
            product = Product(**data)
            db.session.add(product)
    db.session.commit()
    print("✅ Products seeded successfully!")
