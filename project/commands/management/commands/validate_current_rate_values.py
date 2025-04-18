from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from p2p.models import (
    FiatExchangePair,
)


class Command(BaseCommand):
    help = "store possible new rate values for each FiatExchangePair"

    def handle(self, *args, **options):
        pairs = FiatExchangePair.objects.all()

        for pair in pairs:
            if not pair.last_rate:
                continue  # evita error si no hay valor publicado

            market_rate = pair.get_market_rate()
            min_limit = pair.get_market_rate_plus_minimum_margin()
            max_limit = pair.get_last_published_rate_plus_maximum_margin()
            last_rate = pair.last_rate.rate

            if pair.rate_is_inside_min_border() is not True:
                send_mail(
                    subject=f'Par {pair} debajo del mínimo!!',
                    message=(
                        f'Alerta! El valor del par {pair} está fijado en {last_rate} '
                        f'y el valor de mercado está cayendo hasta {market_rate}, '
                        f'traspasando el límite inferior de {min_limit}.'
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_OWNER],
                    fail_silently=False,
                )

            if pair.rate_is_inside_max_border() is not True:
                send_mail(
                    subject=f'Par {pair} encima del máximo!!',
                    message=(
                        f'Alerta! El valor del par {pair} está fijado en {last_rate}, '
                        f'el valor de mercado ha subido hasta {market_rate} y ha excedido '
                        f'el límite superior de {max_limit}.'
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_OWNER],
                    fail_silently=False,
                )

        self.stdout.write("✅ Checkeo de rates concluido.")
