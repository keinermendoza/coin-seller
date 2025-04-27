from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("p2p.urls", namespace="p2p")),
]
