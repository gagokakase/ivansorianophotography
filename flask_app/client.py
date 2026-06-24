from flask import Blueprint, render_template, abort, redirect, url_for
from flask_login import login_required, current_user
from models import Album, AlbumAssignment

client_bp = Blueprint("client", __name__, url_prefix="/client")


@client_bp.route("/gallery")
@login_required
def gallery():
    if current_user.is_admin:
        return redirect(url_for("admin.dashboard"))

    album_assignments = AlbumAssignment.query.filter_by(client_id=current_user.id).all()
    albums = [a.album for a in album_assignments]

    return render_template("client/gallery.html", albums=albums)


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
