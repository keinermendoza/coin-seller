from typing import List
from django.contrib import admin
from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from .base_models import TimeStampedModel
from .currency_models import Currency, CurrencyExchangeConditions
from .fiat_exchange_pair_model import FiatExchangePair


class FiatExchangeDummyPairRate(TimeStampedModel):
    fiat_exchange_pair = models.ForeignKey(
        FiatExchangePair, related_name="dummy_rates", on_delete=models.CASCADE
    )
    rate = models.DecimalField(max_digits=10, decimal_places=3)
    market_rate = models.DecimalField(max_digits=10, decimal_places=3)
    max = models.DecimalField(max_digits=10, decimal_places=3)
    min = models.DecimalField(max_digits=10, decimal_places=3)

    market_buy_conditions = models.ForeignKey(
        CurrencyExchangeConditions,
        related_name="dummy_pair_rates_buy",
        on_delete=models.SET_NULL,
        null=True,
    )
    market_sell_conditions = models.ForeignKey(
        CurrencyExchangeConditions,
        related_name="dummy_pair_rates_sell",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        ordering = ["-created"]
