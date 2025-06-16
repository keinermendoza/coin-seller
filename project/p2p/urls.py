from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views
from . import api

app_name = "p2p"
urlpatterns = [
    path("api/fiat-exchange-pairs", api.FiatExchangePairListAPIView.as_view(), name="fiat_exchange_pairs"),
    path("api/refetch-currency-exchange-conditions", api.ReadMarketConditions.as_view(), name="fiat_exchange_pairs"),
    
    
    path("api/fiat-exchange-pairs/<slug:slug>", api.FiatExchangePairMarketAPIView.as_view(), name="fiat_exchange_pair_market"),

    
    path("api/trade-requests", api.TradeRequestView.as_view(), name="trade_requests"),
    path("api/trade-requests/register-exchange", api.ExchangeAPIView.as_view(), name="register_exchange"),
    path("api/trade-requests/update-exchange/<int:pk>", api.ExchangeUpdateAPIView.as_view(), name="register_exchange"),

    path("api/changes", api.CalculatorRatesApiView.as_view(), name="ves_changes_data"),
    path(
        "api/rates/autoupdate",
        api.RatesAutoUpdateAction.as_view(),
        name="rates_autoupdate",
    ),
    path("api/images", api.ImageCoordinatesView.as_view(), name="images"),
    re_path(r"^client.*$", views.ClientView.as_view(), name="react_client"),
    path("", RedirectView.as_view(url="client", permanent=False)),
]
