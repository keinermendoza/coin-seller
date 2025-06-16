from datetime import timedelta, time, datetime
from p2p.models import CurrencyExchangeConditions
from django.utils import timezone as tz
from django.core.management import BaseCommand
from django.utils.timezone import make_aware


class Command(BaseCommand):
    help = "Removes CurrencyExchangeConditions records from more than 3 days"

    def handle(self, *args, **options):
        old_data = CurrencyExchangeConditions.objects.filter(created__lte=tz.now()-timedelta(days=3))
        for data in old_data:
            data.delete()

        self.stdout.write(f"Removing currency exchange conditions from 3 days old")
