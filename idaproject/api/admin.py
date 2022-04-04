from django.contrib import admin
from .models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "url",
        "picture",
        "width",
        "height",
        "parent_picture",
    )
    search_fields = ("id", "name", "parent_picture")
    list_filter = ("id", "name")


# Register your models here.
admin.site.register(Image, ImageAdmin)