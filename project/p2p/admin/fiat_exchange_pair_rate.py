import csv
from django.utils import timezone as tz

from django.urls import reverse
from django.utils.html import format_html
from django.contrib import (
    admin,
)
from decimal import Decimal, ROUND_HALF_UP

from p2p.models import (
    FiatExchangePairRate,
)


@admin.register(FiatExchangePairRate)
class FiatExchangePairRateAdmin(admin.ModelAdmin):
    list_display = [
        "par",
        "created_f",
        "rate",
        "buy_conditions",
        "sell_conditions",
        "conditions_time",
        "sell_price_limit",
        "buy_price_limit",
        "market_now",
        "market_time",
    ]
    list_filter = ["fiat_exchange_pair"]

    def created_f(self, obj):
        return tz.localtime(obj.created).strftime("%d/%m/%Y %H:%M")

    created_f.short_description = "Created"

    def conditions_time(self, obj):
        if obj.market_buy_conditions and obj.market_sell_conditions:
            return tz.localtime(obj.market_buy_conditions.created).strftime(
                "%d/%m/%Y %H:%M"
            )

    def par(self, obj):
        return obj.fiat_exchange_pair

    def market_now(self, obj):
        return obj.fiat_exchange_pair.get_market_rate()

    def market_time(self, obj):
        currency_from = (
            obj.fiat_exchange_pair.currency_from.exchange_conditions.filter(
                operation_type="B",
            )
            .order_by("-created")
            .first()
        )

        if currency_from:
            return tz.localtime(currency_from.created).strftime("%d/%m/%Y %H:%M")

    def buy_conditions(self, obj):
        if obj.market_buy_conditions:
            price = obj.market_buy_conditions.price
            symbol = obj.market_buy_conditions.currency.symbol
            minimum = obj.market_buy_conditions.extra_data_listing.get(
                "minSingleTransAmount", " - "
            )

            url = reverse(
                "admin:p2p_currencyexchangeconditions_change",
                args=[obj.market_buy_conditions.id],
            )
            return format_html(
                f'<a href="{url}">{symbol} {price} desde {minimum}uds</a>'
            )

    buy_conditions.short_description = "Comprando a"

    def sell_conditions(self, obj):
        if obj.market_sell_conditions:
            price = obj.market_sell_conditions.price
            symbol = obj.market_sell_conditions.currency.symbol
            minimum = obj.market_sell_conditions.extra_data_listing.get(
                "minSingleTransAmount", " - "
            )

            url = reverse(
                "admin:p2p_currencyexchangeconditions_change",
                args=[obj.market_sell_conditions.id],
            )
            return format_html(
                f'<a href="{url}">{symbol} {price} desde {minimum}uds</a>'
            )

    sell_conditions.short_description = "Vendiendo a"
