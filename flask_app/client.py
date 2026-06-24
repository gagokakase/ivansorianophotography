from flask import Blueprint, render_template, abort, redirect, url_for, request, flash, send_from_directory, current_app
from flask_login import login_required, current_user
from models import db, Album, AlbumAssignment, PhotoAssignment, User, Photo
from utils import sanitize_text, sanitize_password, validate_email, MAX_NAME_LENGTH
import os

client_bp = Blueprint("client", __name__, url_prefix="/client")


@client_bp.route("/gallery")
@login_required
def gallery():
    if current_user.is_admin:
        return redirect(url_for("admin.dashboard"))

    album_assignments = AlbumAssignment.query.filter_by(client_id=current_user.id).all()
    albums = [a.album for a in album_assignments]

    return render_template("client/gallery.html", albums=albums)


@client_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if current_user.is_admin:
        return redirect(url_for("admin.profile"))

    if request.method == "POST":
        action = request.form.get("action") or "update_info"
        name = sanitize_text(request.form.get("name"), max_length=MAX_NAME_LENGTH)
        email = (request.form.get("email") or "").strip().lower()
        password = sanitize_password(request.form.get("password"))
        current_password = sanitize_password(request.form.get("current_password"))

        if action == "change_password":
            if not current_user.password_hash:
                flash("Your account uses social login. Password change is not available.", "error")
                return redirect(url_for("client.profile"))
            if not current_password:
                flash("Current password is required.", "error")
                return redirect(url_for("client.profile"))
            if not current_user.check_password(current_password):
                flash("Current password is incorrect.", "error")
                return redirect(url_for("client.profile"))
            if not password or len(password) < 6:
                flash("New password must be at least 6 characters.", "error")
                return redirect(url_for("client.profile"))
            current_user.set_password(password)
            db.session.commit()
            flash("Password updated successfully.", "success")
            return redirect(url_for("client.profile"))

        if not name or not email:
            flash("Name and email are required.", "error")
            return redirect(url_for("client.profile"))
        if not validate_email(email):
            flash("Please enter a valid email address.", "error")
            return redirect(url_for("client.profile"))

        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != current_user.id:
            flash("An account with this email already exists.", "error")
            return redirect(url_for("client.profile"))

        current_user.name = name
        current_user.email = email
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("client.profile"))

    album_assignments = AlbumAssignment.query.filter_by(client_id=current_user.id).all()
    total_albums = len(album_assignments)
    photo_assignments = PhotoAssignment.query.filter_by(client_id=current_user.id).count()

    return render_template("client/profile.html",
                           total_albums=total_albums,
                           total_photos=photo_assignments)


@client_bp.route("/album/<int:album_id>")
@login_required
def view_album(album_id):
    if current_user.is_admin:
        return redirect(url_for("admin.dashboard"))

    assignment = AlbumAssignment.query.filter_by(album_id=album_id, client_id=current_user.id).first()
    if not assignment:
        abort(403)

    album = assignment.album
    photos = [ap.photo for ap in album.photos]
    return render_template("client/album.html", album=album, photos=photos)


@client_bp.route("/photo/<int:photo_id>")
@login_required
def view_photo(photo_id):
    if current_user.is_admin:
        return redirect(url_for("admin.dashboard"))

    assignment = PhotoAssignment.query.filter_by(photo_id=photo_id, client_id=current_user.id).first()
    if not assignment:
        abort(403)

    return render_template("client/view_photo.html", photo=assignment.photo)


@client_bp.route("/download/<int:photo_id>")
@login_required
def download_photo(photo_id):
    if current_user.is_admin:
        return redirect(url_for("admin.dashboard"))

    photo = Photo.query.get_or_404(photo_id)

    assignment = PhotoAssignment.query.filter_by(photo_id=photo_id, client_id=current_user.id).first()
    if not assignment:
        album_assignment = AlbumAssignment.query.filter_by(client_id=current_user.id).first()
        if not album_assignment:
            abort(403)

    upload_dir = current_app.config["UPLOAD_FOLDER"]
    originals_dir = os.path.join(upload_dir, "originals")

    # Try to find the original file by matching the webp base name with any extension
    base_name = os.path.splitext(photo.filename)[0]
    original_filename = None
    if os.path.exists(originals_dir):
        for f in os.listdir(originals_dir):
            if os.path.splitext(f)[0] == base_name:
                original_filename = f
                break

    if original_filename:
        return send_from_directory(originals_dir, original_filename, as_attachment=True, download_name=photo.original_name)

    # Fallback: serve the WebP if no original exists
    return send_from_directory(upload_dir, photo.filename, as_attachment=True, download_name=photo.original_name)
