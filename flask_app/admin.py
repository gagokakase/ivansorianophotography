import os
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, User, Photo, PhotoAssignment, Album, AlbumPhoto, AlbumAssignment, AlbumCoverPhoto, AdminLog
from utils import sanitize_text, sanitize_password, validate_email, allowed_file, allowed_file_size, MAX_NAME_LENGTH, MAX_DESCRIPTION_LENGTH, MAX_TITLE_LENGTH
from image_utils import optimize_image, get_avif_filename

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            return redirect(url_for("client.gallery"))
        return f(*args, **kwargs)
    return decorated


def log_action(user_id, action, detail=None):
    entry = AdminLog(user_id=user_id, action=action, detail=detail)
    db.session.add(entry)
    db.session.commit()


@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    total_clients = User.query.filter_by(role="client").count()
    total_albums = Album.query.count()
    total_assignments = AlbumAssignment.query.count()
    total_photos = Photo.query.count()
    recent_photos = Photo.query.order_by(Photo.uploaded_at.desc()).limit(6).all()

    # Calculate storage usage
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    originals_dir = os.path.join(upload_dir, "originals")
    storage_limit = 500 * 1024 * 1024  # 500 MB limit

    optimized_size = 0
    originals_size = 0

    if os.path.exists(upload_dir):
        for f in os.listdir(upload_dir):
            fp = os.path.join(upload_dir, f)
            if os.path.isfile(fp):
                optimized_size += os.path.getsize(fp)

    if os.path.exists(originals_dir):
        for f in os.listdir(originals_dir):
            fp = os.path.join(originals_dir, f)
            if os.path.isfile(fp):
                originals_size += os.path.getsize(fp)

    total_storage = optimized_size + originals_size
    storage_pct = min(100, (total_storage / storage_limit * 100)) if storage_limit > 0 else 0

    def fmt_size(bytes):
        if bytes < 1024:
            return f"{bytes} B"
        elif bytes < 1024 * 1024:
            return f"{bytes / 1024:.1f} KB"
        else:
            return f"{bytes / (1024 * 1024):.1f} MB"

    return render_template("admin/dashboard.html",
                           total_clients=total_clients,
                           total_albums=total_albums,
                           total_assignments=total_assignments,
                           total_photos=total_photos,
                           recent_photos=recent_photos,
                           storage_used=fmt_size(total_storage),
                           storage_optimized=fmt_size(optimized_size),
                           storage_originals=fmt_size(originals_size),
                           storage_limit=fmt_size(storage_limit),
                           storage_pct=round(storage_pct, 1))


@admin_bp.route("/profile", methods=["GET", "POST"])
@admin_required
def profile():
    if request.method == "POST":
        action = request.form.get("action") or "update_info"
        name = sanitize_text(request.form.get("name"), max_length=MAX_NAME_LENGTH)
        email = (request.form.get("email") or "").strip().lower()
        password = sanitize_password(request.form.get("password"))
        current_password = sanitize_password(request.form.get("current_password"))

        if action == "change_password":
            if not current_password:
                flash("Current password is required.", "error")
                return redirect(url_for("admin.profile"))
            if not current_user.check_password(current_password):
                flash("Current password is incorrect.", "error")
                return redirect(url_for("admin.profile"))
            if not password or len(password) < 6:
                flash("New password must be at least 6 characters.", "error")
                return redirect(url_for("admin.profile"))
            current_user.set_password(password)
            db.session.commit()
            log_action(current_user.id, "password_change")
            flash("Password updated successfully.", "success")
            return redirect(url_for("admin.profile"))

        # Default: update info
        if not name or not email:
            flash("Name and email are required.", "error")
            return redirect(url_for("admin.profile"))
        if not validate_email(email):
            flash("Please enter a valid email address.", "error")
            return redirect(url_for("admin.profile"))

        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != current_user.id:
            flash("An account with this email already exists.", "error")
            return redirect(url_for("admin.profile"))

        current_user.name = name
        current_user.email = email
        db.session.commit()
        log_action(current_user.id, "profile_update", f"Name: {name}, Email: {email}")
        flash("Profile updated successfully.", "success")
        return redirect(url_for("admin.profile"))

    total_albums = Album.query.filter_by(created_by=current_user.id).count()
    total_clients = User.query.filter_by(role="client").count()
    total_photos = Photo.query.filter_by(uploaded_by=current_user.id).count()

    return render_template("admin/profile.html",
                           total_albums=total_albums,
                           total_clients=total_clients,
                           total_photos=total_photos)


@admin_bp.route("/clients")
@admin_required
def clients():
    client_list = User.query.filter_by(role="client").order_by(User.created_at.desc()).all()
    return render_template("admin/clients.html", clients=client_list)


@admin_bp.route("/clients/create", methods=["POST"])
@admin_required
def create_client():
    name = sanitize_text(request.form.get("name"), max_length=MAX_NAME_LENGTH)
    email = (request.form.get("email") or "").strip().lower()
    password = sanitize_password(request.form.get("password"))

    if not name or not email or not password:
        flash("All fields are required.", "error")
        return redirect(url_for("admin.clients"))
    if not validate_email(email):
        flash("Please enter a valid email address.", "error")
        return redirect(url_for("admin.clients"))

    if User.query.filter_by(email=email).first():
        flash("An account with this email already exists.", "error")
        return redirect(url_for("admin.clients"))

    user = User(name=name, email=email, role="client")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    log_action(current_user.id, "client_create", f"Client: {name} ({email})")

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

    name = sanitize_text(request.form.get("name"), max_length=MAX_NAME_LENGTH)
    email = (request.form.get("email") or "").strip().lower()
    password = sanitize_password(request.form.get("password"))

    if not name or not email:
        flash("Name and email are required.", "error")
        return redirect(url_for("admin.clients"))
    if not validate_email(email):
        flash("Please enter a valid email address.", "error")
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
    log_action(current_user.id, "client_edit", f"Client ID {client_id}: {name} ({email})")
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
    log_action(current_user.id, "client_delete", f"Client ID {client_id}")
    return jsonify({"success": True, "message": "Client deleted."})


@admin_bp.route("/photos")
@admin_required
def photos():
    return redirect(url_for("admin.albums"))


@admin_bp.route("/photos/upload", methods=["POST"])
@admin_required
def upload_photo():
    if "files" not in request.files:
        flash("No files selected.", "error")
        return redirect(url_for("admin.photos"))

    files = request.files.getlist("files")
    title = sanitize_text(request.form.get("title"), max_length=MAX_TITLE_LENGTH)

    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"])
    originals_dir = os.path.join(upload_dir, "originals")
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(originals_dir, exist_ok=True)

    uploaded = 0
    for f in files:
        if f and f.filename and allowed_file(f.filename):
            if not allowed_file_size(f):
                flash(f"File '{f.filename}' exceeds the 20MB size limit.", "error")
                continue
            original = secure_filename(f.filename)
            # Add timestamp to avoid collisions
            import time
            saved_name = f"{int(time.time())}_{original}"
            original_path = os.path.join(originals_dir, saved_name)
            f.save(original_path)

            # Convert to optimized AVIF
            avif_name = get_avif_filename(saved_name)
            avif_path = os.path.join(upload_dir, avif_name)
            optimize_image(original_path, avif_path)

            photo = Photo(filename=avif_name, original_name=original, title=title, uploaded_by=current_user.id)
            db.session.add(photo)
            uploaded += 1

    if uploaded > 0:
        db.session.commit()
        log_action(current_user.id, "photo_upload", f"{uploaded} photo(s), title: {title}")
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
    # Also remove original from backup folder
    original_filename = os.path.splitext(photo.filename)[0] + os.path.splitext(photo.original_name)[1]
    original_filepath = os.path.join(upload_dir, "originals", original_filename)
    if os.path.exists(original_filepath):
        os.remove(original_filepath)

    db.session.delete(photo)
    db.session.commit()
    log_action(current_user.id, "photo_delete", f"Photo ID {photo_id}")
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


# ---- Album management ----

@admin_bp.route("/albums")
@admin_required
def albums():
    all_albums = Album.query.order_by(Album.created_at.desc()).all()
    all_clients = User.query.filter_by(role="client").order_by(User.name).all()
    return render_template("admin/albums.html", albums=all_albums, clients=all_clients)


@admin_bp.route("/albums/create", methods=["POST"])
@admin_required
def create_album():
    name = sanitize_text(request.form.get("name"), max_length=200)
    description = sanitize_text(request.form.get("description"), max_length=MAX_DESCRIPTION_LENGTH)

    if not name:
        flash("Album name is required.", "error")
        return redirect(url_for("admin.albums"))

    album = Album(name=name, description=description, created_by=current_user.id)
    db.session.add(album)
    db.session.commit()
    log_action(current_user.id, "album_create", f"Album: {name}")

    flash(f"Album '{name}' created.", "success")
    return redirect(url_for("admin.albums"))


@admin_bp.route("/albums/<int:album_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_album(album_id):
    album = Album.query.get_or_404(album_id)

    if request.method == "GET":
        return jsonify({
            "id": album.id,
            "name": album.name,
            "description": album.description or ""
        })

    name = sanitize_text(request.form.get("name"), max_length=200)
    description = sanitize_text(request.form.get("description"), max_length=MAX_DESCRIPTION_LENGTH)

    if not name:
        flash("Album name is required.", "error")
        return redirect(url_for("admin.albums"))

    album.name = name
    album.description = description
    db.session.commit()
    log_action(current_user.id, "album_edit", f"Album ID {album_id}: {name}")
    flash(f"Album '{name}' updated.", "success")
    return redirect(url_for("admin.albums"))


@admin_bp.route("/albums/<int:album_id>")
@admin_required
def album_detail(album_id):
    album = Album.query.get_or_404(album_id)
    all_photos = Photo.query.order_by(Photo.uploaded_at.desc()).all()
    album_photo_ids = [ap.photo_id for ap in album.photos]
    all_clients = User.query.filter_by(role="client").order_by(User.name).all()
    assigned_client_ids = [a.client_id for a in album.assignments]
    return render_template("admin/album_detail.html",
                           album=album,
                           all_photos=all_photos,
                           album_photo_ids=album_photo_ids,
                           all_clients=all_clients,
                           assigned_client_ids=assigned_client_ids)


@admin_bp.route("/albums/<int:album_id>/upload", methods=["POST"])
@admin_required
def upload_to_album(album_id):
    album = Album.query.get_or_404(album_id)

    if "files" not in request.files:
        return jsonify({"success": False, "message": "No files selected."}), 400

    files = request.files.getlist("files")
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"])
    originals_dir = os.path.join(upload_dir, "originals")
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(originals_dir, exist_ok=True)

    uploaded = 0
    for f in files:
        if f and f.filename and allowed_file(f.filename):
            if not allowed_file_size(f):
                continue
            original = secure_filename(f.filename)
            import time
            saved_name = f"{int(time.time())}_{uploaded}_{original}"
            original_path = os.path.join(originals_dir, saved_name)
            f.save(original_path)

            # Convert to optimized AVIF
            avif_name = get_avif_filename(saved_name)
            avif_path = os.path.join(upload_dir, avif_name)
            optimize_image(original_path, avif_path)

            photo = Photo(filename=avif_name, original_name=original, uploaded_by=current_user.id)
            db.session.add(photo)
            db.session.flush()

            ap = AlbumPhoto(album_id=album.id, photo_id=photo.id)
            db.session.add(ap)
            uploaded += 1

    if uploaded > 0:
        db.session.commit()
        return jsonify({"success": True, "message": f"{uploaded} photo(s) uploaded and added to album."})
    else:
        return jsonify({"success": False, "message": "No valid image files were uploaded."}), 400


@admin_bp.route("/albums/<int:album_id>/photos", methods=["POST"])
@admin_required
def add_photos_to_album(album_id):
    album = Album.query.get_or_404(album_id)
    photo_ids = request.get_json(force=True).get("photo_ids", [])

    added = 0
    for pid in photo_ids:
        existing = AlbumPhoto.query.filter_by(album_id=album.id, photo_id=pid).first()
        if not existing:
            ap = AlbumPhoto(album_id=album.id, photo_id=pid)
            db.session.add(ap)
            added += 1

    db.session.commit()
    return jsonify({"success": True, "message": f"{added} photo(s) added to album."})


@admin_bp.route("/albums/<int:album_id>/photos/<int:photo_id>", methods=["DELETE"])
@admin_required
def remove_photo_from_album(album_id, photo_id):
    ap = AlbumPhoto.query.filter_by(album_id=album_id, photo_id=photo_id).first()
    if ap:
        db.session.delete(ap)
        db.session.commit()
    return jsonify({"success": True, "message": "Photo removed from album."})


@admin_bp.route("/albums/<int:album_id>/cover", methods=["POST"])
@admin_required
def set_album_cover(album_id):
    album = Album.query.get_or_404(album_id)
    data = request.get_json(force=True)

    layout = data.get("layout", "single")
    photo_ids = data.get("photo_ids", [])

    if layout == "single":
        photo_id = data.get("photo_id")
        if photo_id:
            ap = AlbumPhoto.query.filter_by(album_id=album.id, photo_id=photo_id).first()
            if not ap:
                return jsonify({"success": False, "message": "Photo is not in this album."}), 400
            album.cover_photo_id = photo_id
        album.cover_position_x = data.get("position_x", 50.0)
        album.cover_position_y = data.get("position_y", 50.0)
        album.cover_zoom = data.get("zoom", 1.0)
    else:
        album.cover_photo_id = None

    album.cover_layout = layout

    # Replace cover photos
    AlbumCoverPhoto.query.filter_by(album_id=album.id).delete()
    for i, pid in enumerate(photo_ids):
        ap = AlbumPhoto.query.filter_by(album_id=album.id, photo_id=pid).first()
        if ap:
            album_cover = AlbumCoverPhoto(album_id=album.id, photo_id=pid, position=i)
            db.session.add(album_cover)

    db.session.commit()
    log_action(current_user.id, "cover_update", f"Album ID {album_id}, layout: {layout}")
    return jsonify({"success": True, "message": "Cover updated."})


@admin_bp.route("/albums/<int:album_id>/reorder", methods=["POST"])
@admin_required
def reorder_photos(album_id):
    album = Album.query.get_or_404(album_id)
    data = request.get_json(force=True)
    photo_ids = data.get("photo_ids", [])

    for i, pid in enumerate(photo_ids):
        ap = AlbumPhoto.query.filter_by(album_id=album.id, photo_id=pid).first()
        if ap:
            ap.order_index = i

    db.session.commit()
    log_action(current_user.id, "photo_reorder", f"Album ID {album_id}")
    return jsonify({"success": True, "message": "Photo order updated."})


@admin_bp.route("/albums/<int:album_id>/assign", methods=["POST"])
@admin_required
def assign_album(album_id):
    album = Album.query.get_or_404(album_id)
    data = request.get_json(force=True)
    client_ids = data.get("client_ids", [])

    AlbumAssignment.query.filter_by(album_id=album.id).delete()
    for cid in client_ids:
        aa = AlbumAssignment(album_id=album.id, client_id=cid)
        db.session.add(aa)

    db.session.commit()
    log_action(current_user.id, "album_assign", f"Album ID {album_id}, clients: {len(client_ids)}")
    return jsonify({"success": True, "message": f"Album assigned to {len(client_ids)} client(s)."})


@admin_bp.route("/albums/<int:album_id>/assignments")
@admin_required
def get_album_assignments(album_id):
    assignments = AlbumAssignment.query.filter_by(album_id=album_id).all()
    return jsonify({"client_ids": [a.client_id for a in assignments]})


@admin_bp.route("/albums/<int:album_id>", methods=["DELETE"])
@admin_required
def delete_album(album_id):
    album = Album.query.get_or_404(album_id)
    name = album.name
    db.session.delete(album)
    db.session.commit()
    log_action(current_user.id, "album_delete", f"Album: {name}")
    return jsonify({"success": True, "message": f"Album '{name}' deleted."})


@admin_bp.route("/logs")
@admin_required
def logs():
    page = request.args.get("page", 1, type=int)
    per_page = 50
    pagination = AdminLog.query.order_by(AdminLog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template("admin/logs.html", logs=pagination.items, pagination=pagination)
