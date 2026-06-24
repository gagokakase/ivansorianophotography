from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="client")  # 'admin' or 'client'
    name = db.Column(db.String(100), nullable=False, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    assignments = db.relationship("PhotoAssignment", backref="client", foreign_keys="PhotoAssignment.client_id", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == "admin"


class Photo(db.Model):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(200), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    uploader = db.relationship("User", foreign_keys=[uploaded_by])
    assignments = db.relationship("PhotoAssignment", backref="photo", cascade="all, delete-orphan")


class PhotoAssignment(db.Model):
    __tablename__ = "photo_assignments"

    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey("photos.id"), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("photo_id", "client_id", name="uq_photo_client"),)


class Album(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    creator = db.relationship("User", foreign_keys=[created_by])
    photos = db.relationship("AlbumPhoto", backref="album", cascade="all, delete-orphan", order_by="AlbumPhoto.added_at.desc()")
    assignments = db.relationship("AlbumAssignment", backref="album", cascade="all, delete-orphan")


class AlbumPhoto(db.Model):
    __tablename__ = "album_photos"

    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"), nullable=False)
    photo_id = db.Column(db.Integer, db.ForeignKey("photos.id"), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    photo = db.relationship("Photo")

    __table_args__ = (db.UniqueConstraint("album_id", "photo_id", name="uq_album_photo"),)


class AlbumAssignment(db.Model):
    __tablename__ = "album_assignments"

    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)

    client = db.relationship("User", foreign_keys=[client_id])

    __table_args__ = (db.UniqueConstraint("album_id", "client_id", name="uq_album_client"),)
