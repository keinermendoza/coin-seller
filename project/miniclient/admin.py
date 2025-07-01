from django.contrib import admin
from .models import SimpleRate

@admin.register(SimpleRate)
class SimpleRateAdmin(admin.ModelAdmin):
    list_display = [
        "base_currency",
        "target_currency",
        "rate",
        "is_default",
        "base_amount",
        "target_amount",
        "updated_at",
    ]
    list_editable = ["rate", "base_amount","target_amount", "is_default"]