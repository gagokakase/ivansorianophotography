import json
import os
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True, port=5000)
