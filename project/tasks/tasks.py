import logging
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command # NEW


logger = get_task_logger(__name__)

@shared_task
def fetch_binance():
    call_command("retrive_data_from_binance")
    call_command("store_dummie_rates_for_exchange_pairs")
    call_command("validate_current_rate_values")

