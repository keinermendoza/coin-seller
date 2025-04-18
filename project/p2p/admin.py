from django.contrib import (
    admin,
    messages
)
from decimal import Decimal, ROUND_HALF_UP

from .models import (
    Currency,
    CurrencyExchangeConditions,
    CurrencyOperationPreferences,
    FiatExchangePair,
    FiatExchangeDummyPairRate
)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created", "edited")

@admin.register(CurrencyExchangeConditions)
class CurrencyExchangeConditionsAdmin(admin.ModelAdmin):
    list_filter = ["currency", "operation_type"]
    list_display = [
        "currency",
        "created",
        "price",
        "operation_type",
        "time_limit",
        "minimum",
        "maximum",
        "publisher_name",
    ]

    def time_limit(self, obj):
        return f"{obj.extra_data_listing.get('payTimeLimit', ' - ')}  min"

    def minimum(self, obj):
        return f"{obj.extra_data_listing.get('minSingleTransAmount', ' - ')}  {obj.currency.symbol}"

    def maximum(self, obj):
        return f"{obj.extra_data_listing.get('maxSingleTransAmount', ' - ')}  {obj.currency.symbol}"

@admin.register(CurrencyOperationPreferences)
class CurrencyOperationPreferencesAdmin(admin.ModelAdmin):
    pass

@admin.register(FiatExchangePair)
class FiatExchangePairAdmin(admin.ModelAdmin):
    list_display = [
        "par",
        "rate_is_inside_min_border",
        "rate_is_inside_max_border",
        "publicado",
        "minimo",
        "valor_mercado",
        "maximo",
        "hora_publicado",
        "hora_mercado",
    ]

    actions = ["actualizar_tipo_de_cambio"]

    def par(self, obj):
        return f"{obj.currency_from.code}/{obj.currency_to.code}"
    
    
    def valor_mercado(self, obj):
        if rate := obj.get_market_rate():
            return rate.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
        
    def minimo(self, obj):
        if min := obj.get_market_rate_plus_minimum_margin():
            return min.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
        
    def maximo(self, obj):
        if max := obj.get_last_published_rate_plus_maximum_margin():
            return max.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
        
    def hora_mercado(self, obj):
        currency_from = obj.currency_from.exchange_conditions.filter(
            operation_type='B',
        ).order_by('-created').first()

        if currency_from:
            return currency_from.created
        
    def publicado(self, obj):
        if obj.last_rate:
            return obj.last_rate.rate.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
        
    def hora_publicado(self, obj):
        if obj.last_rate:
            return obj.last_rate.created

    def actualizar_tipo_de_cambio(modeladmin, request, queryset):
        for fiat_pair in queryset:
            fiat_pair.create_rate()

        modeladmin.message_user(
            request,
            f"nuevos tipos de cambios actualizado con exitos",
            messages.SUCCESS
        )


@admin.register(FiatExchangeDummyPairRate)
class FiatExchangeDummyPairRateAdmin(admin.ModelAdmin):
    list_display = [
        "par",
        "created",
        "rate",
        "min",
        "market_old",
        "max",
        "market_now",
        "market_time",
    ]
    list_filter = ["fiat_exchange_pair"]


    def par(self, obj):
        return obj.fiat_exchange_pair
    
    def market_now(self, obj):
        if rate := obj.fiat_exchange_pair.get_market_rate():
            return rate.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
    
    def market_old(self, obj):
        return obj.market_rate.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
    
    def market_time(self, obj):
        return obj.fiat_exchange_pair.last_rate.created

    