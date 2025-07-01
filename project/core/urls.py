from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("images/", include("image_creation.urls")),
    path("", include("miniclient.urls")),
    path("", include("p2p.urls", namespace="p2p")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
