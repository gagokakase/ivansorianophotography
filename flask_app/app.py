import json
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "isp-secret-key-change-in-production")
app.config["UPLOAD_FOLDER"] = os.environ.get("UPLOAD_FOLDER", os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "uploads"))

database_url = os.environ.get("DATABASE_URL") or os.environ.get("MYSQL_URL")
if database_url:
    if database_url.startswith("mysql://"):
        database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)
    elif database_url.startswith("mysql+pymysql://"):
        pass
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "site.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
app.config["SESSION_COOKIE_DURATION"] = timedelta(minutes=30)
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(minutes=30)
app.config["WTF_CSRF_TIME_LIMIT"] = 3600
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PREFERRED_URL_SCHEME"] = "https"
if os.environ.get("RAILWAY_PUBLIC_DOMAIN"):
    app.config["SERVER_NAME"] = os.environ["RAILWAY_PUBLIC_DOMAIN"]

# OAuth credentials from environment
app.config["FB_APP_ID"] = os.environ.get("FB_APP_ID", "")
app.config["FB_APP_SECRET"] = os.environ.get("FB_APP_SECRET", "")
app.config["GOOGLE_CLIENT_ID"] = os.environ.get("GOOGLE_CLIENT_ID", "")
app.config["GOOGLE_CLIENT_SECRET"] = os.environ.get("GOOGLE_CLIENT_SECRET", "")

csrf = CSRFProtect(app)

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

# Exempt OAuth callback routes from CSRF
csrf.exempt(app.view_functions["auth.facebook_login"])
csrf.exempt(app.view_functions["auth.facebook_callback"])
csrf.exempt(app.view_functions["auth.google_login"])
csrf.exempt(app.view_functions["auth.google_callback"])

# Exempt client export-selected route (download-only, no state changes)
if "client.export_selected" in app.view_functions:
    csrf.exempt(app.view_functions["client.export_selected"])


# Ensure upload directory exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


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


def send_inquiry_email(data):
    """Send inquiry data to the photographer's Gmail via SMTP."""
    gmail_user = os.environ.get("GMAIL_USER", "")
    gmail_password = os.environ.get("GMAIL_APP_PASSWORD", "")
    recipient = "ics.photog@gmail.com"
    if not gmail_user or not gmail_password:
        return False

    subject = f"New Inquiry from {data['name']} - {data['eventType'].title()}"

    html_body = f"""\
<html>
<body style="margin:0;padding:0;background-color:#080C09;font-family:'Inter',system-ui,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#080C09;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background-color:#111714;border:1px solid rgba(200,169,110,0.15);border-radius:12px;overflow:hidden;">
          <!-- Header -->
          <tr>
            <td style="background-color:#1F4830;padding:28px 40px;border-bottom:1px solid rgba(200,169,110,0.2);">
              <h1 style="margin:0;color:#C8A96E;font-size:22px;font-weight:500;letter-spacing:0.05em;">New Inquiry Received</h1>
              <p style="margin:6px 0 0 0;color:#9DAD9F;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;">Ivan Soriano Photography</p>
            </td>
          </tr>
          <!-- Body -->
          <tr>
            <td style="padding:32px 40px;">
              <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
                <tr>
                  <td style="padding:12px 0;border-bottom:1px solid rgba(200,169,110,0.08);width:140px;vertical-align:top;">
                    <span style="color:#9DAD9F;font-size:13px;text-transform:uppercase;letter-spacing:0.1em;">Name</span>
                  </td>
                  <td style="padding:12px 0;border-bottom:1px solid rgba(200,169,110,0.08);color:#F5F0E1;font-size:16px;vertical-align:top;">
                    {data['name']}
                  </td>
                </tr>
                <tr>
                  <td style="padding:12px 0;border-bottom:1px solid rgba(200,169,110,0.08);vertical-align:top;">
                    <span style="color:#9DAD9F;font-size:13px;text-transform:uppercase;letter-spacing:0.1em;">Email</span>
                  </td>
                  <td style="padding:12px 0;border-bottom:1px solid rgba(200,169,110,0.08);vertical-align:top;">
                    <a href="mailto:{data['email']}" style="color:#C8A96E;font-size:16px;text-decoration:none;">{data['email']}</a>
                  </td>
                </tr>
                <tr>
                  <td style="padding:12px 0;border-bottom:1px solid rgba(200,169,110,0.08);vertical-align:top;">
                    <span style="color:#9DAD9F;font-size:13px;text-transform:uppercase;letter-spacing:0.1em;">Phone</span>
                  </td>
                  <td style="padding:12px 0;border-bottom:1px solid rgba(200,169,110,0.08);color:#F5F0E1;font-size:16px;vertical-align:top;">
                    {data['phone'] or 'Not provided'}
                  </td>
                </tr>
                <tr>
                  <td style="padding:12px 0;border-bottom:1px solid rgba(200,169,110,0.08);vertical-align:top;">
                    <span style="color:#9DAD9F;font-size:13px;text-transform:uppercase;letter-spacing:0.1em;">Event Type</span>
                  </td>
                  <td style="padding:12px 0;border-bottom:1px solid rgba(200,169,110,0.08);color:#F5F0E1;font-size:16px;vertical-align:top;">
                    {data['eventType'].title()}
                  </td>
                </tr>
                <tr>
                  <td style="padding:12px 0;border-bottom:1px solid rgba(200,169,110,0.08);vertical-align:top;">
                    <span style="color:#9DAD9F;font-size:13px;text-transform:uppercase;letter-spacing:0.1em;">Event Date</span>
                  </td>
                  <td style="padding:12px 0;border-bottom:1px solid rgba(200,169,110,0.08);color:#F5F0E1;font-size:16px;vertical-align:top;">
                    {data['eventDate'] or 'Not specified'}
                  </td>
                </tr>
              </table>

              <!-- Message -->
              <div style="margin-top:24px;padding:20px;background-color:#0D120F;border:1px solid rgba(200,169,110,0.1);border-radius:8px;">
                <p style="margin:0 0 10px 0;color:#9DAD9F;font-size:13px;text-transform:uppercase;letter-spacing:0.1em;">Message</p>
                <p style="margin:0;color:#F5F0E1;font-size:15px;line-height:1.8;white-space:pre-wrap;">{data['message']}</p>
              </div>
            </td>
          </tr>
          <!-- Footer -->
          <tr>
            <td style="padding:20px 40px;background-color:#0D120F;border-top:1px solid rgba(200,169,110,0.08);">
              <p style="margin:0;color:#9DAD9F;font-size:12px;text-align:center;letter-spacing:0.05em;">
                This inquiry was submitted from the Ivan Soriano Photography website contact form.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

    plain_body = (
        f"New inquiry received from the website contact form.\n\n"
        f"Name: {data['name']}\n"
        f"Email: {data['email']}\n"
        f"Phone: {data['phone'] or 'Not provided'}\n"
        f"Event Type: {data['eventType']}\n"
        f"Event Date: {data['eventDate'] or 'Not specified'}\n"
        f"\nMessage:\n{data['message']}\n"
    )

    msg = MIMEMultipart("alternative")
    msg["From"] = gmail_user
    msg["To"] = recipient
    msg["Reply-To"] = data["email"]
    msg["Subject"] = subject
    msg.attach(MIMEText(plain_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, recipient, msg.as_string())
        return True
    except Exception as e:
        print(f"SMTP error: {e}")
        return False


def send_otp_email(to_email, otp_code):
    """Send a 6-digit OTP code to the user's email via SMTP."""
    gmail_user = os.environ.get("GMAIL_USER", "")
    gmail_password = os.environ.get("GMAIL_APP_PASSWORD", "")
    if not gmail_user or not gmail_password:
        return False

    subject = "Your Login Code - Ivan Soriano Photography"

    html_body = f"""\
<html>
<body style="margin:0;padding:0;background-color:#080C09;font-family:'Inter',system-ui,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#080C09;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="480" cellpadding="0" cellspacing="0" style="background-color:#111714;border:1px solid rgba(200,169,110,0.15);border-radius:12px;overflow:hidden;">
          <tr>
            <td style="background-color:#1F4830;padding:24px 40px;border-bottom:1px solid rgba(200,169,110,0.2);text-align:center;">
              <h1 style="margin:0;color:#C8A96E;font-size:20px;font-weight:500;letter-spacing:0.05em;">Login Verification</h1>
              <p style="margin:6px 0 0 0;color:#9DAD9F;font-size:12px;letter-spacing:0.1em;text-transform:uppercase;">Ivan Soriano Photography</p>
            </td>
          </tr>
          <tr>
            <td style="padding:36px 40px;text-align:center;">
              <p style="margin:0 0 24px 0;color:#F5F0E1;font-size:15px;line-height:1.7;">Use the code below to complete your login. This code expires in 5 minutes.</p>
              <div style="display:inline-block;padding:20px 40px;background-color:#0D120F;border:1px solid rgba(200,169,110,0.2);border-radius:10px;">
                <span style="font-size:36px;font-weight:600;letter-spacing:0.4em;color:#C8A96E;font-family:'Inter',monospace;">{otp_code}</span>
              </div>
              <p style="margin:24px 0 0 0;color:#9DAD9F;font-size:13px;">If you didn't request this code, you can safely ignore this email.</p>
            </td>
          </tr>
          <tr>
            <td style="padding:16px 40px;background-color:#0D120F;border-top:1px solid rgba(200,169,110,0.08);">
              <p style="margin:0;color:#9DAD9F;font-size:11px;text-align:center;letter-spacing:0.05em;">This is an automated message from Ivan Soriano Photography.</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

    plain_body = f"Your login code for Ivan Soriano Photography is: {otp_code}\n\nThis code expires in 5 minutes."

    msg = MIMEMultipart("alternative")
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(plain_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"OTP email error: {e}")
        return False


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
@csrf.exempt
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
    delivery_method = (data.get("deliveryMethod") or "email").strip().lower()

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

    inquiry_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "eventType": event_type,
        "eventDate": event_date,
        "message": message,
        "deliveryMethod": delivery_method,
    }

    save_inquiry(inquiry_data)

    if delivery_method == "email":
        email_sent = send_inquiry_email(inquiry_data)
        if email_sent:
            return jsonify({"success": True, "message": "Inquiry sent to Ivan's email! He'll be in touch soon.", "deliveryMethod": "email"})
        else:
            return jsonify({"success": True, "message": "Inquiry saved! Ivan will be in touch soon.", "deliveryMethod": "email"})
    else:
        return jsonify({"success": True, "message": "Opening Messenger...", "deliveryMethod": "messenger"})


# Create tables and seed admin on startup
with app.app_context():
    db.create_all()
    seed_admin()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
