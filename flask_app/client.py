from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from models import Photo, PhotoAssignment

client_bp = Blueprint("client", __name__, url_prefix="/client")


@client_bp.route("/gallery")
@login_required
def gallery():
    if current_user.is_admin:
        from flask import redirect, url_for
        return redirect(url_for("admin.dashboard"))

    assignments = PhotoAssignment.query.filter_by(client_id=current_user.id).all()
    photos = [a.photo for a in assignments]
    return render_template("client/gallery.html", photos=photos)


@client_bp.route("/photo/<int:photo_id>")
@login_required
def view_photo(photo_id):
    if current_user.is_admin:
        from flask import redirect, url_for
        return redirect(url_for("admin.dashboard"))

    assignment = PhotoAssignment.query.filter_by(photo_id=photo_id, client_id=current_user.id).first()
    if not assignment:
        abort(403)

    return render_template("client/view_photo.html", photo=assignment.photo)
