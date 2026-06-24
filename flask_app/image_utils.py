import os
from PIL import Image


def optimize_image(input_path, output_path):
    """Convert an image to high-quality WebP at original resolution.

    Args:
        input_path: Path to the original image file.
        output_path: Path where the optimized WebP should be saved.

    Returns:
        The output_path on success.
    """
    img = Image.open(input_path)

    # Handle transparency: flatten RGBA onto white background
    if img.mode in ("RGBA", "LA", "P"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        background.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
        img = background
    elif img.mode != "RGB":
        img = img.convert("RGB")

    img.save(
        output_path,
        "WEBP",
        quality=90,
        method=6,
    )

    return output_path


def get_webp_filename(original_filename):
    """Convert a filename to its .webp equivalent, preserving the base name.

    Args:
        original_filename: e.g. '1234_photo.jpg'

    Returns:
        e.g. '1234_photo.webp'
    """
    base, _ = os.path.splitext(original_filename)
    return base + ".webp"
