import csv
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import (
    admin,
)
from p2p.models import (
    FiatExchangeDummyPairRate,
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
