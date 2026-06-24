import os
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, User, Photo, PhotoAssignment

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            return redirect(url_for("client.gallery"))
        return f(*args, **kwargs)
    return decorated


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    total_clients = User.query.filter_by(role="client").count()
    total_photos = Photo.query.count()
    total_assignments = PhotoAssignment.query.count()
    recent_photos = Photo.query.order_by(Photo.uploaded_at.desc()).limit(6).all()
    return render_template("admin/dashboard.html",
                           total_clients=total_clients,
                           total_photos=total_photos,
                           total_assignments=total_assignments,
                           recent_photos=recent_photos)


@admin_bp.route("/clients")
@admin_required
def clients():
    client_list = User.query.filter_by(role="client").order_by(User.created_at.desc()).all()
    return render_template("admin/clients.html", clients=client_list)


@admin_bp.route("/clients/create", methods=["POST"])
@admin_required
def create_client():
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""

    if not name or not email or not password:
        flash("All fields are required.", "error")
        return redirect(url_for("admin.clients"))

    if User.query.filter_by(email=email).first():
        flash("An account with this email already exists.", "error")
        return redirect(url_for("admin.clients"))

    user = User(name=name, email=email, role="client")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    flash(f"Client account created for {name}.", "success")
    return redirect(url_for("admin.clients"))


@admin_bp.route("/clients/<int:client_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_client(client_id):
    client = User.query.get_or_404(client_id)
    if client.is_admin:
        return jsonify({"success": False, "message": "Cannot edit admin account."}), 403

    if request.method == "GET":
        return jsonify({
            "id": client.id,
            "name": client.name,
            "email": client.email
        })

    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""

    if not name or not email:
        flash("Name and email are required.", "error")
        return redirect(url_for("admin.clients"))

    existing = User.query.filter_by(email=email).first()
    if existing and existing.id != client.id:
        flash("An account with this email already exists.", "error")
        return redirect(url_for("admin.clients"))

    client.name = name
    client.email = email
    if password:
        client.set_password(password)

    db.session.commit()
    flash(f"Client {name} updated successfully.", "success")
    return redirect(url_for("admin.clients"))


@admin_bp.route("/clients/<int:client_id>", methods=["DELETE"])
@admin_required
def delete_client(client_id):
    client = User.query.get_or_404(client_id)
    if client.is_admin:
        return jsonify({"success": False, "message": "Cannot delete admin account."}), 403

    db.session.delete(client)
    db.session.commit()
    return jsonify({"success": True, "message": "Client deleted."})


@admin_bp.route("/photos")
@admin_required
def photos():
    all_photos = Photo.query.order_by(Photo.uploaded_at.desc()).all()
    all_clients = User.query.filter_by(role="client").order_by(User.name).all()
    return render_template("admin/photos.html", photos=all_photos, clients=all_clients)


@admin_bp.route("/photos/upload", methods=["POST"])
@admin_required
def upload_photo():
    if "files" not in request.files:
        flash("No files selected.", "error")
        return redirect(url_for("admin.photos"))

    files = request.files.getlist("files")
    title = (request.form.get("title") or "").strip()

    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"])
    os.makedirs(upload_dir, exist_ok=True)

    uploaded = 0
    for f in files:
        if f and f.filename and allowed_file(f.filename):
            original = secure_filename(f.filename)
            # Add timestamp to avoid collisions
            import time
            filename = f"{int(time.time())}_{original}"
            filepath = os.path.join(upload_dir, filename)
            f.save(filepath)

            photo = Photo(filename=filename, original_name=original, title=title, uploaded_by=current_user.id)
            db.session.add(photo)
            uploaded += 1

    if uploaded > 0:
        db.session.commit()
        flash(f"{uploaded} photo(s) uploaded successfully.", "success")
    else:
        flash("No valid image files were uploaded.", "error")

    return redirect(url_for("admin.photos"))


@admin_bp.route("/photos/<int:photo_id>", methods=["DELETE"])
@admin_required
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    filepath = os.path.join(upload_dir, photo.filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    db.session.delete(photo)
    db.session.commit()
    return jsonify({"success": True, "message": "Photo deleted."})


@admin_bp.route("/photos/<int:photo_id>/assign", methods=["POST"])
@admin_required
def assign_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    data = request.get_json(force=True)
    client_ids = data.get("client_ids", [])

    added = 0
    for cid in client_ids:
        existing = PhotoAssignment.query.filter_by(photo_id=photo.id, client_id=cid).first()
        if not existing:
            assignment = PhotoAssignment(photo_id=photo.id, client_id=cid)
            db.session.add(assignment)
            added += 1

    db.session.commit()
    return jsonify({"success": True, "message": f"Photo assigned to {added} client(s)."})


@admin_bp.route("/photos/<int:photo_id>/assign/<int:client_id>", methods=["DELETE"])
@admin_required
def unassign_photo(photo_id, client_id):
    assignment = PhotoAssignment.query.filter_by(photo_id=photo_id, client_id=client_id).first()
    if assignment:
        db.session.delete(assignment)
        db.session.commit()
    return jsonify({"success": True, "message": "Photo unassigned."})


@admin_bp.route("/photos/<int:photo_id>/assignments")
@admin_required
def get_assignments(photo_id):
    assignments = PhotoAssignment.query.filter_by(photo_id=photo_id).all()
    return jsonify({"client_ids": [a.client_id for a in assignments]})
