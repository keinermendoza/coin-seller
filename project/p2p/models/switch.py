from django.db import models

class SwitchModel(models.Model):
    store_currency_exchange_conditions = models.BooleanField(default=False)
    store_fiat_exchange_dummy_pair_rate = models.BooleanField(default=False)
    email_alert_when_rates_are_out_of_range = models.BooleanField(default=False)
