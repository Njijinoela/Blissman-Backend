from flask import Blueprint, request, jsonify
from config import db
from Models.product import Product

product_bp = Blueprint("product_bp", __name__, url_prefix="/products")

# Helper: serialize product
def serialize_product(product):
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": float(product.price),   # convert Decimal → float
        "image_url": product.image_url,
        "availability": product.availability,
        "category": product.category,
        "specs": product.specs,
        "features": product.features,
        "warranty": product.warranty,
    }

# Get all products
@product_bp.route("/", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([serialize_product(p) for p in products])

# Add a new product
@product_bp.route("/", methods=["POST"])
def add_product():
    data = request.json
    product = Product(
        name=data["name"],
        description=data.get("description"),
        price=data["price"],
        image_url=data.get("image_url"),
        availability=data.get("availability"),
        category=data.get("category"),
        specs=data.get("specs"),
        features=data.get("features"),
        warranty=data.get("warranty"),
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product added", "id": product.id}), 201

# Get single product
@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(serialize_product(product))

# Update product
@product_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json
    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.image_url = data.get("image_url", product.image_url)
    product.availability = data.get("availability", product.availability)
    product.category = data.get("category", product.category)
    product.specs = data.get("specs", product.specs)
    product.features = data.get("features", product.features)
    product.warranty = data.get("warranty", product.warranty)
    db.session.commit()
    return jsonify({"message": "Product updated"})

# Delete product
@product_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"})
