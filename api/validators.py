import os
import pathlib
from django.core.exceptions import ValidationError


MIN_EXPIRY_TIME = os.environ.get('MIN_EXPIRY_LINK_TIME')
MAX_EXPIRY_TIME = os.environ.get('MAX_EXPIRY_LINK_TIME')


def validate_img_extension(image):
    extensions = ['.png', '.jpg']
    image_extension = pathlib.Path(image).suffix
    if image_extension not in extensions:
        raise ValidationError("""this extension is not supported.
                              Supported formats .png .jpg""")


def validate_expiration_time(time):
    if not (MIN_EXPIRY_TIME <= time <= MAX_EXPIRY_TIME):
        raise ValidationError(f"""Expiration time must be in the range
                              {MIN_EXPIRY_TIME} to {MAX_EXPIRY_TIME} """)
