from django.contrib import admin
from p2p.models import ImageCoordinates


@admin.register(ImageCoordinates)
class ImageCoordinatesAdmin(admin.ModelAdmin):
    pass
