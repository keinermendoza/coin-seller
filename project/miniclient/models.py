from django.db import models
from p2p.models.currency_models import Currency

class SimpleRate(models.Model):
    base_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='base_rates'
    )
    target_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='target_rates'
    )
    rate = models.DecimalField(max_digits=10, decimal_places=6)
    updated_at = models.DateTimeField(auto_now=True)
    is_default = models.BooleanField(default=False)
    base_amount = models.DecimalField(max_digits=10, decimal_places=6)
    target_amount = models.DecimalField(max_digits=10, decimal_places=6)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['base_currency', 'target_currency'],
                name='unique_currency_pair'
            )
        ]

    def __str__(self):
        return f"{self.base_currency} → {self.target_currency} = {self.rate}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "base_name": self.base_currency.name,
            "base_symbol": self.base_currency.symbol,
            "base_image": self.base_currency.image.url if self.base_currency.image else "",
            "target_name": self.target_currency.name,
            "target_symbol": self.target_currency.symbol,
            "target_image": self.target_currency.image.url if self.target_currency.image else "",
            "rate": float(self.rate),
            "base_amount": float(self.base_amount),
            "target_amount": float(self.target_amount),
            "is_default": self.is_default,
            "updated_at": self.updated_at
        }