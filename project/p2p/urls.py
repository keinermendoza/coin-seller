from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views
from . import api
app_name = "p2p"
urlpatterns = [
    path("api/sell", api.SellDataView.as_view(), name="sell_data"),
    path("api/changes", api.VESRatesApiView.as_view(), name="ves_changes_data"),
    path("api/rates/autoupdate", api.RatesAutoUpdateAction.as_view(), name="rates_autoupdate"),
    path("api/buy", api.BuyDataView.as_view(), name="buy_data"),
    path("api/images", api.ImageCoordinatesView.as_view(), name="images"),
    re_path(r'^client.*$', views.ClientView.as_view(), name="react_client"),
    path("", RedirectView.as_view(url="client", permanent=False))
]