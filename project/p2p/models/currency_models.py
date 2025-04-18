from django.db import models
from .base_models import TimeStampedModel

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Currency(TimeStampedModel):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    code = models.CharField(max_length=10)
    image = models.ImageField(upload_to="currencies", null=True, blank=True)

    def __str__(self):
        return self.name

class CurrencyOperationPreferences(models.Model):
    currency = models.OneToOneField(Currency, related_name="operation_preferences", on_delete=models.CASCADE)
    filter_for_buy_usdt = models.JSONField()
    filter_for_sell_usdt = models.JSONField()

    def __str__(self):
        return f"Preferences for {self.currency.code}"


class CurrencyExchangeConditions(TimeStampedModel):
    class OperationType(models.TextChoices):
        BUY = "B", "Buy"
        SELL = "S", "Sell"

    currency = models.ForeignKey(Currency, related_name="exchange_conditions", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=3)
    publisher_name = models.CharField(max_length=100, blank=True)
    operation_type = models.CharField(
        verbose_name="type",
        max_length=1,
        choices=OperationType.choices,
        default=OperationType.BUY
    )
    extra_data_listing = models.JSONField(null=True, blank=True)
    extra_data_publisher = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_operation_type_display()} {self.currency.code} @ {self.price} by {self.publisher_name}"
    
    class Meta:
        ordering = ["-created"]
