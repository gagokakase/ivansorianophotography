from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, AdminLog
from utils import sanitize_text, sanitize_password, validate_email, MAX_NAME_LENGTH

auth_bp = Blueprint("auth", __name__)

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION = timedelta(minutes=15)
SESSION_DURATION = timedelta(minutes=30)


def log_action(user_id, action, detail=None):
    entry = AdminLog(user_id=user_id, action=action, detail=detail)
    db.session.add(entry)
    db.session.commit()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("client.gallery"))

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = sanitize_password(request.form.get("password"))

        user = User.query.filter_by(email=email).first()

        if user and user.locked_until and user.locked_until > datetime.utcnow():
            remaining = user.locked_until - datetime.utcnow()
            minutes = int(remaining.total_seconds() // 60)
            flash(f"Account locked due to too many failed attempts. Try again in {minutes} minute(s).", "error")
            return render_template("login.html")

        if user and user.check_password(password):
            user.failed_login_count = 0
            user.locked_until = None
            db.session.commit()
            login_user(user, duration=SESSION_DURATION)
            log_action(user.id, "login_success")
            if user.is_admin:
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("client.gallery"))

        if user:
            user.failed_login_count = (user.failed_login_count or 0) + 1
            if user.failed_login_count >= MAX_FAILED_ATTEMPTS:
                user.locked_until = datetime.utcnow() + LOCKOUT_DURATION
                db.session.commit()
                log_action(user.id, "account_locked", f"Locked after {user.failed_login_count} failed attempts")
                flash("Account locked due to too many failed attempts. Try again in 15 minutes.", "error")
            else:
                db.session.commit()
                log_action(user.id, "login_failed", f"Attempt {user.failed_login_count}/{MAX_FAILED_ATTEMPTS}")
                remaining = MAX_FAILED_ATTEMPTS - user.failed_login_count
                flash(f"Invalid email or password. {remaining} attempt(s) remaining.", "error")
        else:
            flash("Invalid email or password.", "error")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("client.gallery"))

    if request.method == "POST":
        name = sanitize_text(request.form.get("name"), max_length=MAX_NAME_LENGTH)
        email = (request.form.get("email") or "").strip().lower()
        password = sanitize_password(request.form.get("password"))
        confirm = sanitize_password(request.form.get("confirm"))

        errors = {}
        if not name:
            errors["name"] = "Name is required."
        if not email:
            errors["email"] = "Email is required."
        elif not validate_email(email):
            errors["email"] = "Please enter a valid email address."
        elif User.query.filter_by(email=email).first():
            errors["email"] = "An account with this email already exists."
        if not password:
            errors["password"] = "Password is required."
        elif len(password) < 6:
            errors["password"] = "Password must be at least 6 characters."
        if password != confirm:
            errors["confirm"] = "Passwords do not match."

        if errors:
            for field, msg in errors.items():
                flash(msg, "error")
            return render_template("register.html", name=name, email=email)

        user = User(name=name, email=email, role="client")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user, duration=SESSION_DURATION)
        return redirect(url_for("client.gallery"))

    return render_template("register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    log_action(current_user.id, "logout")
    logout_user()
    return redirect(url_for("index"))
