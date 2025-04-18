from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from p2p.models import (
    Currency,
    FiatExchangePair
)


class Command(BaseCommand):
    help = "seeds database"

    def handle(self, *args, **options):
        bolivar = Currency.objects.get(
            name="Bolivar"
        )

        real = Currency.objects.get(
            name="Real"
        )

        try:
            FiatExchangePair.objects.create(
                currency_from=bolivar,
                currency_to=real,
                optimum_margin_expected=4.5,
                minimum_margin_expected=2,
                maximum_margin_limit=6.5
            )
           
        except IntegrityError:
            self.stderr.write("saltando creacion de par VES/BRL posible presencia en base de datos") # NEW

        try:
            FiatExchangePair.objects.create(
                currency_from=real,
                currency_to=bolivar,
                optimum_margin_expected=4.5,
                minimum_margin_expected=2,
                maximum_margin_limit=6.5,

            )

                  
        except IntegrityError:
            self.stderr.write("saltando creacion de par BRL/VES posible presencia en base de datos") # NEW

        self.stdout.write("seeder ejecutado") # NEW
    


