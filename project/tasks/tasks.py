import logging
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command  # NEW
from p2p.models import SwitchModel

logger = get_task_logger(__name__)


@shared_task
def fetch_binance():
    switch = SwitchModel.objects.first()
    if switch.store_currency_exchange_conditions:
        call_command("retrive_data_from_binance")
    if switch.store_currency_exchange_conditions:
        call_command("store_dummie_rates_for_exchange_pairs")
    if switch.email_alert_when_rates_are_out_of_range:
        call_command("email_alert_discontinuated_rates")


@shared_task
def remove_old_data():
    switch = SwitchModel.objects.first()

    if switch.destroy_old_currency_exchange_conditions:
        call_command("remove_old_currency_exchange_conditions")
