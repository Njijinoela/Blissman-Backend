from flask import Blueprint, request, jsonify
from config import db
from Models.order import Order, OrderItem
from Models.product import Product
from Models.user import User
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from threading import Thread

load_dotenv()

order_bp = Blueprint("order_bp", __name__, url_prefix="/orders")

# Helper function to send emails
def send_email(to, subject, body, html=False):
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    smtp_host = os.environ.get("EMAIL_SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("EMAIL_SMTP_PORT", 465))

    if not sender or not password:
        raise RuntimeError("Email sender or password not set in environment variables")

    msg = MIMEText(body, "html" if html else "plain")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to

    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(sender, password)
        server.sendmail(sender, [to], msg.as_string())


# Run email sending in a background thread
def async_send_email(to, subject, body, html=False):
    Thread(target=send_email, args=(to, subject, body, html), daemon=True).start()


# Create a new order
@order_bp.route("/", methods=["POST"])
def create_order():
    data = request.json
    print("📥 Incoming order:", data)  # <-- debug

    customer_id = data.get("customer_id")
    items = data.get("items", [])
    phone = data.get("phone")
    email = data.get("email")

    if not items or not phone or not email:
        return jsonify({"error": "Missing items, phone, or email"}), 400

    total = 0
    order = Order(customer_id=customer_id, total_amount=0, phone=phone, email=email)
    db.session.add(order)
    db.session.flush()  # get order.id before commit

    order_summary = []
    for item in items:
        product = Product.query.get(item["product_id"])
        if not product:
            return jsonify({"error": f"Product {item['product_id']} not found"}), 404

        qty = int(item.get("quantity", 1))
        price = float(product.price)  # ensure numeric
        total += price * qty
        db.session.add(OrderItem(order_id=order.id, product_id=product.id, quantity=qty))
        order_summary.append(f"- {product.name} (x{qty}) @ KES {price}")

    order.total_amount = total
    db.session.commit()

    # Build order text
    order_text = f"""
    New Order Received

    Phone: {phone}
    Email: {email}

    Items:
    {chr(10).join(order_summary)}

    Total: KES {total}
    """

    try:
        send_email(os.environ.get("COMPANY_EMAIL"), f"New Order #{order.id}", order_text)
        send_email(email, f"Your Order Confirmation #{order.id}", order_text)
    except Exception as e:
        print("❌ Email sending failed:", e)

    return jsonify({
        "message": "Order created successfully",
        "order_id": order.id,
        "total": total
    }), 201
