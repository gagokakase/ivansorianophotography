import json
import os
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "isp-secret-key-change-in-production")
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "uploads")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "site.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
from models import db, User

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Register blueprints
from auth import auth_bp
from admin import admin_bp
from client import client_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(client_bp)


# Ensure upload directory exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


INQUIRIES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inquiries.json")


def save_inquiry(data):
    inquiries = []
    if os.path.exists(INQUIRIES_FILE):
        try:
            with open(INQUIRIES_FILE, "r", encoding="utf-8") as f:
                inquiries = json.load(f)
        except (json.JSONDecodeError, IOError):
            inquiries = []
    data["submitted_at"] = datetime.utcnow().isoformat() + "Z"
    inquiries.append(data)
    with open(INQUIRIES_FILE, "w", encoding="utf-8") as f:
        json.dump(inquiries, f, indent=2, ensure_ascii=False)


def seed_admin():
    """Create default admin account if none exists."""
    if not User.query.filter_by(role="admin").first():
        admin = User(name="Ivan Soriano", email="ics.photog@gmail.com", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Default admin created: ics.photog@gmail.com / admin123")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/contact", methods=["POST"])
def contact():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"success": False, "message": "Invalid request body."}), 400

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    event_type = (data.get("eventType") or "").strip()
    event_date = (data.get("eventDate") or "").strip()
    message = (data.get("message") or "").strip()

    errors = {}
    if not name:
        errors["name"] = "Name is required."
    if not email:
        errors["email"] = "Email is required."
    elif not re.match(r"^\S+@\S+$", email):
        errors["email"] = "Please enter a valid email."
    if not event_type:
        errors["eventType"] = "Event type is required."
    if not message:
        errors["message"] = "Message is required."

    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    save_inquiry({
        "name": name,
        "email": email,
        "phone": phone,
        "eventType": event_type,
        "eventDate": event_date,
        "message": message,
    })

    return jsonify({"success": True, "message": "Message sent! Ivan will be in touch soon."})


# Create tables and seed admin on startup
with app.app_context():
    db.create_all()
    seed_admin()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
