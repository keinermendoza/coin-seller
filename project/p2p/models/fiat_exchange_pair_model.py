from decimal import Decimal, ROUND_HALF_UP
from typing import List
from django.contrib import admin
from django.db import models
from django.apps import apps
from .base_models import TimeStampedModel
from .currency_models import Currency, CurrencyExchangeConditions
from django.contrib.auth import get_user_model

User = get_user_model()


class FiatExchangePairQuerySet(models.QuerySet):
    def user_suscribed(self, user: User, **kwargs):
        if prefs_ids := user.fiat_preferences.filter(**kwargs).values_list(
            "pair", flat=True
        ):
            return self.filter(id__in=prefs_ids)
        return self.none()

   


class FiatExchangePairManager(models.Manager):
    def get_queryset(self):
        return FiatExchangePairQuerySet(self.model, using=self._db)

    def user_suscribed(self, user, **kwargs):
        return self.get_queryset().user_suscribed(user, **kwargs)
    
    def user_suscribed_buy_side(self, user: User, **kwargs):
        UserFiatPreferences = apps.get_model("p2p", "UserFiatPreferences")
        return self.user_suscribed(
            user, side_operation=UserFiatPreferences.ExchangeSideOperation.BUY
        )

    def user_suscribed_sell_side(self, user: User, **kwargs):
        UserFiatPreferences = apps.get_model("p2p", "UserFiatPreferences")

        return self.user_suscribed(
            user, side_operation=UserFiatPreferences.ExchangeSideOperation.SELL
        )


class FiatExchangePair(TimeStampedModel):
    slug = models.SlugField(null=True, blank=True)
    currency_from = models.ForeignKey(
        Currency, related_name="exchanges_as_origin", on_delete=models.PROTECT
    )
    currency_to = models.ForeignKey(
        Currency, related_name="exchanges_as_destination", on_delete=models.PROTECT
    )

    optimum_margin_expected = models.DecimalField(max_digits=8, decimal_places=3)
    minimum_margin_expected = models.DecimalField(max_digits=8, decimal_places=3)
    maximum_margin_limit = models.DecimalField(max_digits=8, decimal_places=3)

    objects = FiatExchangePairManager()

    @property
    def maximum_margin(self):
        return self.maximum_margin_limit / 100

    @property
    def minimum_margin(self):
        return self.minimum_margin_expected / 100

    @property
    def optimum_margin(self):
        return self.optimum_margin_expected / 100

    def get_last_currency_exchange_conditions_pair_buy_sell(
        self,
    ) -> List["CurrencyExchangeConditions"]:

        from_currency = (
            self.currency_from.exchange_conditions.filter(
                operation_type="B",
            )
            .order_by("-created")
            .first()
        )

        to_currency = (
            self.currency_to.exchange_conditions.filter(
                operation_type="S",
            )
            .order_by("-created")
            .first()
        )

        return [from_currency, to_currency]

    def get_market_rate(self):
        from_currency, to_currency = (
            self.get_last_currency_exchange_conditions_pair_buy_sell()
        )

        if from_currency and to_currency:
            rate = to_currency.price / from_currency.price
            return Decimal(rate).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

    def get_market_rate_plus_optimum_margin(self) -> Decimal | None:
        if market_rate := self.get_market_rate():
            return market_rate * (1 - self.optimum_margin)

    def get_last_published_rate_plus_maximum_margin(self) -> Decimal | None:
        if self.last_rate:
            return Decimal(self.last_rate.rate * (1 + self.maximum_margin)).quantize(
                Decimal("0.0001"), rounding=ROUND_HALF_UP
            )

    def get_market_rate_plus_minimum_margin(self) -> Decimal | None:
        if market_rate := self.get_market_rate():
            return Decimal(market_rate * (1 - self.minimum_margin)).quantize(
                Decimal("0.0001"), rounding=ROUND_HALF_UP
            )

    @admin.display(boolean=True, description="¿min ok?")
    def rate_is_inside_min_border(self) -> bool | None:
        if minimum_rate := self.get_market_rate_plus_minimum_margin():
            if self.last_rate:
                return minimum_rate >= self.last_rate.rate

    @admin.display(boolean=True, description="¿max ok?")
    def rate_is_inside_max_border(self) -> bool | None:
        if maximum_rate := self.get_last_published_rate_plus_maximum_margin():
            if market_rate := self.get_market_rate():
                return maximum_rate > market_rate

    def create_rate(self, rate: Decimal | None = None) -> "FiatExchangePairRate":
        """
        store a valid published rate
        """

        FiatExchangePairRate = apps.get_model("p2p", "FiatExchangePairRate")

        if rate is None:
            rate = self.get_market_rate_plus_optimum_margin()

        if rate is None:
            raise ValueError("No se pudo calcular un rate de mercado válido.")

        from_currency, to_currency = (
            self.get_last_currency_exchange_conditions_pair_buy_sell()
        )

        return FiatExchangePairRate.objects.create(
            fiat_exchange_pair=self,
            rate=rate,
            market_buy_conditions=from_currency,
            market_sell_conditions=to_currency,
        )

    def store_dummy_rate(
        self, rate: Decimal | None = None
    ) -> "FiatExchangeDummyPairRate":
        """
        creating dummie rates for analytics
        """
        FiatExchangeDummyPairRate = apps.get_model("p2p", "FiatExchangeDummyPairRate")

        if rate is None:
            rate = self.get_market_rate_plus_optimum_margin()

        if rate is None:
            raise ValueError("No se pudo calcular un rate de mercado válido.")
        #
        market_rate = self.get_market_rate()
        from_currency, to_currency = (
            self.get_last_currency_exchange_conditions_pair_buy_sell()
        )

        return FiatExchangeDummyPairRate.objects.create(
            fiat_exchange_pair=self,
            rate=rate,
            market_rate=market_rate,
            max=market_rate * (1 + self.maximum_margin),
            min=market_rate * (1 - self.minimum_margin),
            market_buy_conditions=from_currency,
            market_sell_conditions=to_currency,
        )

    @property
    def last_rate(self) -> "FiatExchangePairRate":
        FiatExchangePairRate = apps.get_model("p2p", "FiatExchangePairRate")

        return FiatExchangePairRate.objects.filter(fiat_exchange_pair=self).first()

    def save(self, *args, **kwargs):
        self.slug = f"{self.currency_from.code.lower()}_{self.currency_to.code.lower()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.currency_from.code}/{self.currency_to.code}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["currency_from", "currency_to"],
                name="unique_currency_pair_direction",
            )
        ]
