from django.core.management.base import BaseCommand, CommandError
from p2p.models import (
    Currency,
    CurrencyOperationPreferences,
)


class Command(BaseCommand):
    help = "seeds database"

    def handle(self, *args, **options):
        bolivar = Currency.objects.create(name="Bolivar", symbol="Bs", code="VES")

        real = Currency.objects.create(name="Real", symbol="R$", code="BRL")

        # craeting bolivar filters
        bolivar_filters = {"payTypes": ["PagoMovil"], "transAmount": 2000}

        CurrencyOperationPreferences.objects.create(
            currency=bolivar,
            filter_for_buy_usdt=bolivar_filters,
            filter_for_sell_usdt=bolivar_filters,
        )

        # craeting real filters
        real_filters = {"payTypes": ["PIX"], "transAmount": 100}

        CurrencyOperationPreferences.objects.create(
            currency=real,
            filter_for_buy_usdt=real_filters,
            filter_for_sell_usdt=real_filters,
        )

        self.stdout.write("seeder ejecutado.")  # NEW
