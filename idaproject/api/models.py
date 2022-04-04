import os
import requests
from django.db import models
from django.core.files.base import ContentFile
from .utils import get_picture_name_from_url


class Image(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    file = models.ImageField(null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    picture = models.CharField(max_length=200, null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    parent_picture = models.PositiveIntegerField(null=True, blank=True)
