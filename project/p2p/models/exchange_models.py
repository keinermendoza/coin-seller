from django.contrib import admin
from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from .base_models import TimeStampedModel
from .currency_models import (
    Currency
)

class FiatExchangePair(TimeStampedModel):
    currency_from = models.ForeignKey(
        Currency,
        related_name="exchanges_as_origin",
        on_delete=models.PROTECT
    )
    currency_to = models.ForeignKey(
        Currency,
        related_name="exchanges_as_destination",
        on_delete=models.PROTECT
    )

    optimum_margin_expected = models.DecimalField(max_digits=8, decimal_places=3)
    minimum_margin_expected = models.DecimalField(max_digits=8, decimal_places=3)
    maximum_margin_limit = models.DecimalField(max_digits=8, decimal_places=3)
    
    @property
    def maximum_margin(self):
        return self.maximum_margin_limit / 100

    @property
    def minimum_margin(self):
        return self.minimum_margin_expected / 100
    
    @property
    def optimum_margin(self):
        return self.optimum_margin_expected / 100

    def get_market_rate(self):
        from_currency = self.currency_from.exchange_conditions.filter(
            operation_type='B',
        ).order_by('-created').first()

        to_currency = self.currency_to.exchange_conditions.filter(
            operation_type='S',
        ).order_by('-created').first()

        if from_currency and to_currency:
            rate =  to_currency.price / from_currency.price 
            return Decimal(rate).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
    
    def get_market_rate_plus_optimum_margin(self) -> Decimal | None:
        if market_rate:= self.get_market_rate():
            return market_rate * (1 - self.optimum_margin) 
    
    def get_last_published_rate_plus_maximum_margin(self) -> Decimal | None:
        if self.last_rate:
            return Decimal(self.last_rate.rate * (1 + self.maximum_margin)).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
         

    def get_market_rate_plus_minimum_margin(self) -> Decimal | None:
        if market_rate:= self.get_market_rate():
            return Decimal(market_rate * (1 - self.minimum_margin)).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP) 
    
    @admin.display(boolean=True, description='¿min ok?')
    def rate_is_inside_min_border(self) -> bool | None:
        if minimum_rate := self.get_market_rate_plus_minimum_margin():
            if self.last_rate:
                return minimum_rate >= self.last_rate.rate 

    @admin.display(boolean=True, description='¿max ok?')
    def rate_is_inside_max_border(self) -> bool | None:
        if maximum_rate := self.get_last_published_rate_plus_maximum_margin():
            if market_rate:= self.get_market_rate():
                return maximum_rate > market_rate 

    def create_rate(self, rate: Decimal | None = None) -> 'FiatExchangePairRate':
        """
        store a valid published rate 
        """
        if rate is None:
            rate = self.get_market_rate_plus_optimum_margin()

        if rate is None:
            raise ValueError("No se pudo calcular un rate de mercado válido.")

        return FiatExchangePairRate.objects.create(
            fiat_exchange_pair=self,
            rate=rate
        )

    def store_dummy_rate(self, rate: Decimal | None = None) -> 'FiatExchangeDummyPairRate':
        """
        creating dummie rates for analytics
        """
        if rate is None:
            rate = self.get_market_rate_plus_optimum_margin()

        if rate is None:
            raise ValueError("No se pudo calcular un rate de mercado válido.")
# 
        market_rate = self.get_market_rate()
        return FiatExchangeDummyPairRate.objects.create(
            fiat_exchange_pair=self,
            rate=rate,
            market_rate=market_rate,
            max=market_rate * (1 + self.maximum_margin),
            min=market_rate * (1 - self.minimum_margin)
        )
    
    @property
    def last_rate(self) -> 'FiatExchangePairRate':
        return FiatExchangePairRate.objects.filter(
            fiat_exchange_pair=self
        ).first()
  
    
    def __str__(self):
        return f"{self.currency_from.code}/{self.currency_to.code}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['currency_from', 'currency_to'],
                name='unique_currency_pair_direction'
            )
        ]
        
class FiatExchangePairRate(TimeStampedModel):
    fiat_exchange_pair = models.ForeignKey(
        FiatExchangePair,
        related_name="rates",
        on_delete=models.CASCADE
    ) 
    rate = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        ordering = ["-created"]


class FiatExchangeDummyPairRate(TimeStampedModel):
    fiat_exchange_pair = models.ForeignKey(
        FiatExchangePair,
        related_name="dummy_rates",
        on_delete=models.CASCADE
    ) 
    rate = models.DecimalField(max_digits=10, decimal_places=3)
    market_rate = models.DecimalField(max_digits=10, decimal_places=3)
    max = models.DecimalField(max_digits=10, decimal_places=3)
    min = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        ordering = ["-created"]