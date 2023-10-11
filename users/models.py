import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from api.models import ThumbnailSize
# Create your models here.


class Tier(models.Model):
    name = models.CharField(max_length=40)
    get_original_file = models.BooleanField(default=False)
    can_generate_expiring_links = models.BooleanField(default=False)
    thumbnail_sizes = models.ManyToManyField(ThumbnailSize)

    def __str__(self):
        return self.name

    @property
    def get_thumbnail_sizes(self):
        return self.thumbnail_sizes.all()

    @property
    def get_available_heights(self):
        thumnails = self.get_thumbnail_sizes
        return [thumbnail.height for thumbnail in thumnails]


class UserCustom(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_tier = models.ForeignKey("Tier", on_delete=models.SET_NULL,
                                  null=True, related_name="users")

    def __str__(self):
        return f"""{self.username} ({self.user_tier.name
                                     if self.user_tier else 'basic'})"""
