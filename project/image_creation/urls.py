from django.urls import path
from . import views

app_label = "image_creation"

urlpatterns = [
    path("download-image", views.ImageBannerView.as_view(), name="download_image"),
]
