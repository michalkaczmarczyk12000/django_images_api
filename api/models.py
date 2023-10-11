import uuid
import os
import time
from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL  # auth.User


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.image}"

    @property
    def get_original_image_url(self):
        return self.image.url

    def extract_avaliable_thumbnails_for_tier(self, thumbnails,
                                              avaliable_sizes):
        avaliable_tier_images = []
        for thumbnail in thumbnails:
            name, _ = os.path.splitext(thumbnail)
            # example filename dog_300.png
            height = name.split("_")[-1]
            # validation if height is digit
            if height.isdigit() and int(height) in avaliable_sizes:
                avaliable_tier_images.append(thumbnail)
        return avaliable_tier_images

    def get_thumbnails(self):
        base_file = os.path.dirname(self.image.name)
        user_tier = self.user.get_tier
        avaliable_thumbnail_sizes = user_tier.get_avaliable_thumbnail_sizes
        all_thumbnails = os.listdir(base_file)

        tier_images = self.extract_avaliable_thumbnails_for_tier
        (all_thumbnails, avaliable_thumbnail_sizes)

        # check if user can get original file

        if user_tier.get_original_file:
            tier_images.append(self.get_original_image_url)

        # check if user can generate expiring link and if expiring_link exist

        if (user_tier.can_generate_expiring_links and
           hasattr(self, 'expiring_link')):
            tier_images.append(self.expiring_link.link)
        return tier_images


class ThumbnailSize(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return f"{self.width}x{self.height}"


class ExpiringLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    link = models.CharField(max_length=255)
    image = models.OneToOneField(Image, on_delete=models.CASCADE,
                                 unique=True,
                                 related_name='expiring_link')
    expires_in = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.link}"

    def is_expired(self):
        return time.time() > self.expires_in
