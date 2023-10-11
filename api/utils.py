import os
import re


def image_upload_path(instance, filename):
    return f"{instance.user.id}/images/{instance.id}/{filename}"


def sanitize_filename(filename):
    basename, ext = os.path.splitext(filename)
    basename = re.sub(r'[^\w\.]', '_', basename)
    filename = f"{basename}{ext}"
    return filename
