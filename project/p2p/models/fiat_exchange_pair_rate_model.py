from typing import List
from django.contrib import admin
from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from .base_models import TimeStampedModel
from .currency_models import Currency, CurrencyExchangeConditions
from .fiat_exchange_pair_model import FiatExchangePair


class FiatExchangePairRate(TimeStampedModel):
    fiat_exchange_pair = models.ForeignKey(
        FiatExchangePair, related_name="rates", on_delete=models.CASCADE
    )
    market_buy_conditions = models.ForeignKey(
        CurrencyExchangeConditions,
        related_name="pair_rates_buy",
        on_delete=models.SET_NULL,
        null=True,
    )
    market_sell_conditions = models.ForeignKey(
        CurrencyExchangeConditions,
        related_name="pair_rates_sell",
        on_delete=models.SET_NULL,
        null=True,
    )

    rate = models.DecimalField(max_digits=10, decimal_places=3)

    def sell_price_limit(self):
        """
        Provides a simplified view of the profitability limit on the sell side of the pair.
        Assumes the buy price remains constant.
        This method does not take the current market price into account.

        For a complete profitability check before executing an operation, see:
        - FiatExchangePair.rate_is_inside_min_border
        - FiatExchangePair.rate_is_inside_max_border
        """
        if self.market_buy_conditions:
            return Decimal(self.market_buy_conditions.price * self.rate).quantize(
                Decimal("0.001"), rounding=ROUND_HALF_UP
            )

    sell_price_limit.short_description = "Vender sobre"

    def buy_price_limit(self):
        """
        Provides a simplified view of the profitability limit on the buy side of the pair.
        Assumes the sell price remains constant.
        This method does not take the current market price into account.

        For a complete profitability check before executing an operation, see:
        - FiatExchangePair.rate_is_inside_min_border
        - FiatExchangePair.rate_is_inside_max_border
        """
        if self.market_sell_conditions:
            return Decimal(self.market_sell_conditions.price / self.rate).quantize(
                Decimal("0.001"), rounding=ROUND_HALF_UP
            )

    buy_price_limit.short_description = "Comprar bajo"

    class Meta:
        ordering = ["-created"]
