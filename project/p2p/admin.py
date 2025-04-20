import csv
from django.http import HttpResponse

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
    FiatExchangePairRate,
    FiatExchangeDummyPairRate,
    SwitchModel
)

@admin.register(SwitchModel)
class SwitchModelAdmin(admin.ModelAdmin):
    pass

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
        "lim_max_publicado",
        "valor_mercado",
        "lim_max_mercado",
        "hora_publicado",
        "hora_mercado",
    ]

    actions = ["actualizar_tipo_de_cambio", "exportar_a_csv"]

    def par(self, obj):
        return f"{obj.currency_from.code}/{obj.currency_to.code}"
    
    def valor_mercado(self, obj):
        return obj.get_market_rate()
        
    def lim_max_publicado(self, obj):
        return obj.get_market_rate_plus_minimum_margin()
        
    def lim_max_mercado(self, obj):
        return obj.get_last_published_rate_plus_maximum_margin()
        
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
    
    def exportar_a_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="fiat_exchange_pairs.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "Par",
            "Dentro del min",
            "Dentro del max",
            "Publicado",
            "Min",
            "Valor Mercado",
            "Max",
            "Hora Publicado",
            "Hora Mercado"
        ])

        for obj in queryset:
            writer.writerow([
                self.par(obj),
                obj.rate_is_inside_min_border,
                obj.rate_is_inside_max_border,
                self.publicado(obj),
                self.minimo(obj),
                self.valor_mercado(obj),
                self.maximo(obj),
                self.hora_publicado(obj),
                self.hora_mercado(obj),
            ])

        return response

    exportar_a_csv.short_description = "Exportar selección a CSV"


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
    actions = ["exportar_a_csv"]


    def par(self, obj):
        return obj.fiat_exchange_pair
    
    def market_now(self, obj):
        return obj.fiat_exchange_pair.get_market_rate()
    
    def market_old(self, obj):
        return obj.market_rate
    
    def market_time(self, obj):
        currency_from = obj.fiat_exchange_pair.currency_from.exchange_conditions.filter(
            operation_type='B',
        ).order_by('-created').first()

        if currency_from:
            return currency_from.created
        
    def exportar_a_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="fiat_exchange_rates.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "Par", "Fecha", "Rate", "Min", "Market Old", "Max", "Market Now", "Market Time"
        ])
        for obj in queryset:
            writer.writerow([
                obj.fiat_exchange_pair,
                obj.created,
                obj.rate,
                obj.min,
                self.market_old(obj),
                obj.max,
                self.market_now(obj),
                self.market_time(obj),
            ])
        return response
    exportar_a_csv.short_description = "Exportar selección a CSV"

    
@admin.register(FiatExchangePairRate)
class FiatExchangePairRateAdmin(admin.ModelAdmin):
    list_display = [
        "par",
        "created",
        "rate",
        "market_now",
        "market_time",
    ]
    list_filter = ["fiat_exchange_pair"]


    def par(self, obj):
        return obj.fiat_exchange_pair
    
    def market_now(self, obj):
        return obj.fiat_exchange_pair.get_market_rate()
  
    def market_time(self, obj):
        currency_from = obj.fiat_exchange_pair.currency_from.exchange_conditions.filter(
            operation_type='B',
        ).order_by('-created').first()

        if currency_from:
            return currency_from.created