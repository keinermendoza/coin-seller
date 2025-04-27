from django.db import models
from p2p.models.base_models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Exchange(TimeStampedModel):
    class ExchangeSideOperation(models.TextChoices):
        BUY = "B", "Buy"
        SELL = "S", "Sell"

    registered_by = models.ForeignKey(
        User, related_name="exchanges", on_delete=models.SET_NULL, null=True, blank=True
    )
    amount = models.DecimalField(
        help_text="amount of currency traded", max_digits=8, decimal_places=3
    )
    price = models.DecimalField(
        help_text="price expresed in the axe asset",
        max_digits=8,
        decimal_places=3,
    )
    side_operation = models.CharField(
        max_length=1,
        choices=ExchangeSideOperation.choices,
        default=ExchangeSideOperation.BUY,
    )

    def __str__(self):
        user = self.registered_by.username if self.registered_by else "Unknown"
        side = self.get_side_operation_display()
        status = self.get_status_display()
        return f"{side} {self.amount} at {self.price} ({status}) by {user}"
