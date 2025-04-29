from django.db import models
from p2p.models import (
    FiatExchangePair,
)
from p2p.models.base_models import TimeStampedModel
from p2p.models.exchange_model import Exchange
from django.contrib.auth import get_user_model

User = get_user_model()


class TradeRequestQuerySet(models.QuerySet):
    def open(self):
        return self.filter(status=self.model.TradeOperationStatus.OPEN)

    def one_side_ready(self):
        return self.filter(status=self.model.TradeOperationStatus.ONE_SIDE_READY)

    def completed(self):
        return self.filter(status=self.model.TradeOperationStatus.COMPLETED)

    def cancelled(self):
        return self.filter(status=self.model.TradeOperationStatus.CANCELLED)

    def ves_to_brl(self):
        return self.filter(pair__slug="ves_brl")

    def brl_to_ves(self):
        return self.filter(pair__slug="brl_ves")

    def user_suscribed(self, user: User):
        if prefs_ids := user.fiat_preferences.values_list("id", flat=True):
            return self.filter(pair__in=prefs_ids)
        return self.none()


class TradeRequestManager(models.Manager):
    def get_queryset(self):
        return TradeRequestQuerySet(self.model, using=self._db)

    def open(self):
        return self.get_queryset().open()

    def one_side_ready(self):
        return self.get_queryset().one_side_ready()

    def completed(self):
        return self.get_queryset().completed()

    def cancelled(self):
        return self.get_queryset().cancelled()

    def ves_to_brl(self):
        return self.get_queryset().ves_to_brl()

    def brl_to_ves(self):
        return self.get_queryset().brl_to_ves()

    def ves_to_brl_pending(self):
        return self.get_queryset().ves_to_brl().open()

    def brl_to_ves_pending(self):
        return self.get_queryset().brl_to_ves().open()
    
    def user_suscribed(self, user):
        return self.get_queryset().user_suscribed(user)

class TradeRequest(TimeStampedModel):
    class TradeOperationStatus(models.IntegerChoices):
        OPEN = 1, "Pendiente"
        ONE_SIDE_READY = 2, "Media operación realizada"
        COMPLETED = 3, "Dinero entregado al destinatario"
        CANCELLED = 4, "Operación cancelada"

    created_by = models.ForeignKey(
        User,
        related_name="trade_requests_registered",
        on_delete=models.SET_NULL,
        null=True,
    )
    requested_amount = models.DecimalField(max_digits=8, decimal_places=3)

    pair = models.ForeignKey(
        FiatExchangePair, related_name="trades", on_delete=models.PROTECT
    )

    exchange_buy = models.OneToOneField(
        Exchange,
        related_name="trade_buy",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    exchange_sell = models.OneToOneField(
        Exchange,
        related_name="trade_sell",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    rate = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    result = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    status = models.PositiveIntegerField(
        choices=TradeOperationStatus.choices, default=TradeOperationStatus.OPEN
    )

    objects = TradeRequestManager()

    def __str__(self):
        return f"TradeRequest: {self.rate} → {self.result} for pair {self.pair}"
