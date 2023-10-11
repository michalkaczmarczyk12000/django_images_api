import tiers_config
import pathlib
from django.core.exceptions import ValidationError


def validate_img_extension(image):
    extensions = ['.png', '.jpg']
    image_extension = pathlib.Path(image).suffix
    if image_extension not in extensions:
        raise ValidationError("""this extension is not supported.
                              Supported formats .png .jpg""")


def validate_expiration_time(time):
    if not (tiers_config.MIN_EXPIRY_LINK_TIME <= time
            <= tiers_config.MAX_EXPIRY_LINK_TIME):
        raise ValidationError(f"""Expiration time must be in the range
                              {tiers_config.MIN_EXPIRY_LINK_TIME} to
                              {tiers_config.MAX_EXPIRY_LINK_TIME} """)
