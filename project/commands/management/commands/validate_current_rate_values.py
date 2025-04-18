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
            if pair.rate_is_inside_min_border() is False:
                send_mail(
                    subject=f'par {pair} debajo del minimo!!',
                    message=f'Alerta! el valor del par {pair} está fijado en {pair.last_rate.rate} y el valor de mercado está cayendo hasta {pair.get_market_rate()} traspasando el limite inferior de {pair.get_market_rate_plus_minimum_margin()}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_OWNER,],
                    fail_silently=False,
                )

            if pair.rate_is_inside_max_border() is False:
                send_mail(
                    subject=f'par {pair} encima del maximo!!',
                    message=f'Alerta! el valor del par {pair} está fijado en {pair.last_rate.rate} el valor de mercado ha subido hasta {pair.get_market_rate()} y excedido el valor maximo de {pair.get_last_published_rate_plus_maximum_margin()} ',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_OWNER,],
                    fail_silently=False,
                )


        self.stdout.write("checkeo de rates concluido") # NEW
