from django.db import models


class Banners(models.Model):
    banner_image = models.ImageField(upload_to="banner_image", null=False, blank=False)
    banner_url = models.URLField(null=False, blank=False)
