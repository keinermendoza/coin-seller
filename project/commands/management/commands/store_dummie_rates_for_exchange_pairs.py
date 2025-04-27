from django.core.management.base import BaseCommand
from p2p.models import (
    FiatExchangePair,
)


class Command(BaseCommand):
    help = "store possible new rate values for each FiatExchangePair"

    def handle(self, *args, **options):
        pairs = FiatExchangePair.objects.all()

        for pair in pairs:
            pair.store_dummy_rate()

            self.stdout.write(f"guardando tipo de cambio posible para {pair}")  # NEW

        self.stdout.write("FiatExchangeDummyPairRate adicionados")  # NEW
