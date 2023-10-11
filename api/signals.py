from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Image
import os
from io import BytesIO
from PIL import Image as PIL_Image
from django.core.files.uploadedfile import SimpleUploadedFile


@receiver(post_save, sender=Image)
def create_thumbnails(sender, instance: Image, **kwargs):
    instance_ = Image.objects.get(id=instance.id)
    filename, ext = os.path.splitext(os.path.basename(instance_.image.name))
    image_name = filename.split("/")[-1]

    user_tier = instance_.user.user_tier
    thumbnail_sizes = user_tier.get_thumbnail_sizes
    for size in thumbnail_sizes:
        img_file = BytesIO(instance_.image.read())
        original_image = PIL_Image.open(img_file)
        thumbnail = original_image.resize((size.width, size.height),
                                          PIL_Image.Resampling.LANCZOS)

        # Save the resized image to the path
        thumb_io = BytesIO()

        thumbnail.save(thumb_io, format="JPEG" if ext.lower() == ".jpg" else "PNG")
        thumbnail_path = f"{image_name}_{size.height}{ext.lower()}"

        thumbnail_file = SimpleUploadedFile(
            thumbnail_path, thumb_io.getvalue(), content_type="image/jpeg" if ext.lower() == ".jpg" else "image/png"
        )
        instance_.image.save(thumbnail_path, thumbnail_file, save=False)
