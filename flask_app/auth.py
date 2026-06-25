from datetime import datetime, timedelta
import os
import secrets
import random
import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, AdminLog
from utils import sanitize_text, sanitize_password, validate_email, MAX_NAME_LENGTH

auth_bp = Blueprint("auth", __name__)

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION = timedelta(minutes=15)
SESSION_DURATION = timedelta(minutes=30)
OTP_EXPIRY = timedelta(minutes=1)


def log_action(user_id, action, detail=None):
    entry = AdminLog(user_id=user_id, action=action, detail=detail)
    db.session.add(entry)
    db.session.commit()


def generate_otp():
    return str(random.randint(100000, 999999))


def start_otp_flow(user):
    from app import send_otp_email
    code = generate_otp()
    session["otp_code"] = code
    session["otp_user_id"] = user.id
    session["otp_email"] = user.email
    session["otp_expiry"] = (datetime.utcnow() + OTP_EXPIRY).isoformat()
    sent = send_otp_email(user.email, code)
    return sent


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("client.gallery"))

    otp_step = session.get("otp_user_id") is not None
    otp_expiry = session.get("otp_expiry") if otp_step else None

    if request.method == "POST":
        step = request.form.get("step", "credentials")

        if step == "otp":
            entered_code = (request.form.get("otp_code") or "").strip()
            stored_code = session.get("otp_code")
            expiry_str = session.get("otp_expiry")

            if not stored_code or not expiry_str:
                flash("Login session expired. Please sign in again.", "error")
                session.pop("otp_code", None)
                session.pop("otp_user_id", None)
                session.pop("otp_email", None)
                session.pop("otp_expiry", None)
                return render_template("login.html", otp_step=False)

            expiry = datetime.fromisoformat(expiry_str)
            if datetime.utcnow() > expiry:
                flash("Verification code expired. Please sign in again.", "error")
                session.pop("otp_code", None)
                session.pop("otp_user_id", None)
                session.pop("otp_email", None)
                session.pop("otp_expiry", None)
                return render_template("login.html", otp_step=False)

            if entered_code == stored_code:
                user_id = session.pop("otp_user_id")
                session.pop("otp_code", None)
                session.pop("otp_email", None)
                session.pop("otp_expiry", None)

                user = User.query.get(user_id)
                if not user:
                    flash("Account not found. Please contact support.", "error")
                    return render_template("login.html", otp_step=False)

                login_user(user, duration=SESSION_DURATION)
                log_action(user.id, "login_success", "via OTP")
                if user.is_admin:
                    return redirect(url_for("admin.dashboard"))
                return redirect(url_for("client.gallery"))
            else:
                flash("Invalid verification code. Please try again.", "error")
                return render_template("login.html", otp_step=True)

        else:
            email = (request.form.get("email") or "").strip().lower()
            password = sanitize_password(request.form.get("password"))

            user = User.query.filter_by(email=email).first()

            if user and user.locked_until and user.locked_until > datetime.utcnow():
                remaining = user.locked_until - datetime.utcnow()
                minutes = int(remaining.total_seconds() // 60)
                flash(f"Account locked due to too many failed attempts. Try again in {minutes} minute(s).", "error")
                return render_template("login.html", otp_step=False)

            if user and user.check_password(password):
                user.failed_login_count = 0
                user.locked_until = None
                db.session.commit()

                sent = start_otp_flow(user)
                if sent:
                    flash("A verification code has been sent to your email.", "success")
                    return render_template("login.html", otp_step=True, otp_expiry=session.get("otp_expiry"))
                else:
                    flash("Could not send verification email. Please try again.", "error")
                    return render_template("login.html", otp_step=False)

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

            return render_template("login.html", otp_step=False)

    return render_template("login.html", otp_step=otp_step, otp_expiry=otp_expiry)


@auth_bp.route("/resend-otp", methods=["POST"])
def resend_otp():
    user_id = session.get("otp_user_id")
    if not user_id:
        flash("Login session expired. Please sign in again.", "error")
        return redirect(url_for("auth.login"))

    user = User.query.get(user_id)
    if not user:
        flash("Account not found. Please sign in again.", "error")
        session.pop("otp_code", None)
        session.pop("otp_user_id", None)
        session.pop("otp_email", None)
        session.pop("otp_expiry", None)
        return redirect(url_for("auth.login"))

    sent = start_otp_flow(user)
    if sent:
        flash("A new verification code has been sent to your email.", "success")
    else:
        flash("Could not resend verification code. Please try again.", "error")

    return redirect(url_for("auth.login"))


@auth_bp.route("/cancel-otp", methods=["POST"])
def cancel_otp():
    session.pop("otp_code", None)
    session.pop("otp_user_id", None)
    session.pop("otp_email", None)
    session.pop("otp_expiry", None)
    return redirect(url_for("auth.login"))


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


# ---- OAuth: Facebook ----

@auth_bp.route("/auth/facebook")
def facebook_login():
    base_url = os.environ.get("OAUTH_REDIRECT_BASE", "").rstrip("/")
    if base_url:
        redirect_uri = base_url + "/auth/facebook/callback"
    else:
        redirect_uri = url_for("auth.facebook_callback", _external=True, _scheme="https")
    print(f"DEBUG Facebook redirect_uri: {redirect_uri}", flush=True)
    state = secrets.token_urlsafe(16)
    fb_app_id = current_app.config["FB_APP_ID"]
    auth_url = (
        f"https://www.facebook.com/v18.0/dialog/oauth"
        f"?client_id={fb_app_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope=public_profile"
        f"&state={state}"
    )
    resp = redirect(auth_url)
    resp.set_cookie("oauth_state", state, httponly=True, samesite="Lax", max_age=600)
    return resp


@auth_bp.route("/auth/facebook/callback")
def facebook_callback():
    code = request.args.get("code")
    if not code:
        flash("Facebook authorization failed.", "error")
        return redirect(url_for("auth.register"))

    base_url = os.environ.get("OAUTH_REDIRECT_BASE", "").rstrip("/")
    if base_url:
        redirect_uri = base_url + "/auth/facebook/callback"
    else:
        redirect_uri = url_for("auth.facebook_callback", _external=True, _scheme="https")
    fb_app_id = current_app.config["FB_APP_ID"]
    fb_app_secret = current_app.config["FB_APP_SECRET"]

    token_resp = requests.get(
        "https://graph.facebook.com/v18.0/oauth/access_token",
        params={
            "client_id": fb_app_id,
            "client_secret": fb_app_secret,
            "redirect_uri": redirect_uri,
            "code": code,
        },
    )
    token_data = token_resp.json()
    access_token = token_data.get("access_token")
    if not access_token:
        flash("Failed to get access token from Facebook.", "error")
        return redirect(url_for("auth.register"))

    user_resp = requests.get(
        "https://graph.facebook.com/me",
        params={"fields": "name,email", "access_token": access_token},
    )
    info = user_resp.json()

    email = (info.get("email") or "").strip().lower()
    name = info.get("name", "")
    fb_id = info.get("id", "")

    if not email and fb_id:
        email = f"fb_{fb_id}@facebook.local"

    if not email:
        flash("Facebook did not return an email. Please use a different method to register.", "error")
        return redirect(url_for("auth.register"))

    user = User.query.filter_by(email=email).first()
    if user:
        login_user(user, duration=SESSION_DURATION)
        log_action(user.id, "login_success", "via Facebook")
        if user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("client.gallery"))

    user = User(name=name, email=email, role="client", oauth_provider="facebook")
    db.session.add(user)
    db.session.commit()
    log_action(user.id, "oauth_register", "via Facebook")
    login_user(user, duration=SESSION_DURATION)
    return redirect(url_for("client.gallery"))


# ---- OAuth: Google ----

@auth_bp.route("/auth/google")
def google_login():
    base_url = os.environ.get("OAUTH_REDIRECT_BASE", "").rstrip("/")
    if base_url:
        redirect_uri = base_url + "/auth/google/callback"
    else:
        redirect_uri = url_for("auth.google_callback", _external=True, _scheme="https")
    print(f"DEBUG Google redirect_uri: {redirect_uri}", flush=True)
    state = secrets.token_urlsafe(16)
    client_id = current_app.config["GOOGLE_CLIENT_ID"]
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope=openid email profile"
        f"&state={state}"
    )
    resp = redirect(auth_url)
    resp.set_cookie("oauth_state", state, httponly=True, samesite="Lax", max_age=600)
    return resp


@auth_bp.route("/auth/google/callback")
def google_callback():
    code = request.args.get("code")
    if not code:
        flash("Google authorization failed.", "error")
        return redirect(url_for("auth.register"))

    base_url = os.environ.get("OAUTH_REDIRECT_BASE", "").rstrip("/")
    if base_url:
        redirect_uri = base_url + "/auth/google/callback"
    else:
        redirect_uri = url_for("auth.google_callback", _external=True, _scheme="https")
    client_id = current_app.config["GOOGLE_CLIENT_ID"]
    client_secret = current_app.config["GOOGLE_CLIENT_SECRET"]

    token_resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
    )
    token_data = token_resp.json()
    access_token = token_data.get("access_token")
    if not access_token:
        flash("Failed to get access token from Google.", "error")
        return redirect(url_for("auth.register"))

    user_resp = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    info = user_resp.json()

    email = (info.get("email") or "").strip().lower()
    name = info.get("name", "")

    if not email:
        flash("Google did not return an email. Please use a different method to register.", "error")
        return redirect(url_for("auth.register"))

    user = User.query.filter_by(email=email).first()
    if user:
        login_user(user, duration=SESSION_DURATION)
        log_action(user.id, "login_success", "via Google")
        if user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("client.gallery"))

    user = User(name=name, email=email, role="client", oauth_provider="google")
    db.session.add(user)
    db.session.commit()
    log_action(user.id, "oauth_register", "via Google")
    login_user(user, duration=SESSION_DURATION)
    return redirect(url_for("client.gallery"))


@auth_bp.route("/logout")
@login_required
def logout():
    log_action(current_user.id, "logout")
    logout_user()
    return redirect(url_for("index"))
