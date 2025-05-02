from django.contrib import admin
from p2p.models import Exchange, TradeRequest


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    pass

@admin.register(TradeRequest)
class TradeRequestAdmin(admin.ModelAdmin):
    list_display = ["pair", "created", "status", "rate", "client_offered_rate", "result", "edited"]
