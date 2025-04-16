from django.contrib import admin

from .models import (
    Currency,
    CurrencyExchangeConditions,
    CurrencyOperationPreferences
)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created", "edited")

@admin.register(CurrencyExchangeConditions)
class CurrencyExchangeConditionsAdmin(admin.ModelAdmin):
    list_filter = ["currency", "opertarion_type_for_usdt"]
    list_display = [
        "currency",
        "created",
        "price",
        "opertarion_type_for_usdt",
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