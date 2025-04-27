from django.db import models
from p2p.models.base_models import TimeStampedModel
from django.contrib.auth import get_user_model
from p2p.models.fiat_exchange_pair_model import FiatExchangePair
from p2p.models.trade_request_model import TradeRequest
from django.core.exceptions import ValidationError

User = get_user_model()


class UserFiatPreferences(TimeStampedModel):
    class ExchangeSideOperation(models.TextChoices):
        BUY = "B", "Buy"
        SELL = "S", "Sell"

    user = models.ForeignKey(
        User,
        related_name="fiat_preferences",
        on_delete=models.CASCADE,
    )
    pair = models.ForeignKey(
        FiatExchangePair,
        related_name="user_fiat_preferences",
        on_delete=models.CASCADE,
    )

    side_operation = models.CharField(
        max_length=1,
        choices=ExchangeSideOperation.choices,
        default=ExchangeSideOperation.BUY,
    )

    def __str__(self):
        user = self.user.username
        side = self.get_side_operation_display()
        pair = self.pair
        return f"{user} suscribes to {pair} in {side} side"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "pair", "side_operation"], name="unique_user_pair_side"
            )
        ]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        if (
            UserFiatPreferences.objects.filter(user=self.user, pair=self.pair)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                "El usuario ya está suscrito a este par con otro side."
            )
