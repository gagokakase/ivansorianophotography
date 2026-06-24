import re
from markupsafe import escape

MAX_NAME_LENGTH = 100
MAX_EMAIL_LENGTH = 120
MAX_DESCRIPTION_LENGTH = 2000
MAX_TITLE_LENGTH = 200

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif", "bmp", "tiff"}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

_EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def sanitize_text(value, max_length=None):
    """Sanitize user text input: strip whitespace, remove null bytes, escape HTML, truncate."""
    if value is None:
        return ""
    text = str(value)
    text = text.replace("\x00", "")
    text = text.strip()
    if max_length:
        text = text[:max_length]
    return str(escape(text))


def sanitize_password(value):
    """Only strip whitespace from passwords — do NOT escape HTML."""
    if value is None:
        return ""
    return str(value).replace("\x00", "").strip()


def validate_email(email):
    """Check if email matches a valid format."""
    if not email:
        return False
    if len(email) > MAX_EMAIL_LENGTH:
        return False
    return bool(_EMAIL_REGEX.match(email))


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def allowed_file_size(file_storage):
    """Check if the uploaded file is within the max size limit."""
    file_storage.seek(0, 2)
    size = file_storage.tell()
    file_storage.seek(0)
    return size <= MAX_FILE_SIZE
