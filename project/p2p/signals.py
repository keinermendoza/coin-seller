from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import TradeRequest

@receiver(pre_save, sender=TradeRequest)
def pre_save_post(sender, instance, update_fields, *args, **kwargs):
    """
    updates the status based on exchange transaction realationship  
    """
    if instance.status is not TradeRequest.TradeStatus.CANCELLED:
        conected_transactions = [instance.exchange_buy, instance.exchange_sell]
        if None not in (conected_transactions):
            instance.status = TradeRequest.TradeStatus.COMPLETED
        elif any(conected_transactions):
            instance.status = TradeRequest.TradeStatus.ONE_SIDE_READY
        elif not any(conected_transactions):
            instance.status = TradeRequest.TradeStatus.OPEN
        