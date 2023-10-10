from django.db import models
import os
from api.models import ThumbnailSize
# Create your models here.


class Tier(models.Model):
    name = models.CharField()
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
