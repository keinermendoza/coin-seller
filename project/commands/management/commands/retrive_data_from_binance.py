import requests as rq
from django.core.management.base import BaseCommand, CommandError
from p2p.models import (
    Currency,
    CurrencyExchangeConditions
)

from binance_client import p2p

class Command(BaseCommand):
    help = "retrives data from binance and save it in db"

    def handle(self, *args, **options):
        currencies = Currency.objects.all()

        for currency in currencies:
            
            # buy petition
            buy_filters = currency.operation_preferences.filter_for_buy_usdt
            resp = p2p.get_listing_for_currency(
                currency=currency.code,
                trade_type="BUY",
                **buy_filters
            )

            data = p2p.extract_relevant_data(resp)
            best_match = data[0] 
            CurrencyExchangeConditions.objects.create(
                currency=currency,
                price=best_match.get("price", ''),
                publisher_name=best_match.get("nickName", ''),
                opertarion_type_for_usdt=CurrencyExchangeConditions.OperationType.BUY,
                extra_data_listing={
                    "payTimeLimit": best_match.get("payTimeLimit", ''),
                    "minSingleTransAmount": best_match.get("minSingleTransAmount", ''),
                    "maxSingleTransAmount": best_match.get("maxSingleTransAmount", ''),
                    "tradeMethods": best_match.get("tradeMethods", ''),

                },
                extra_data_publisher={"positiveRate":best_match.get("positiveRate", '')}
            )

            # sell petition
            sell_filters = currency.operation_preferences.filter_for_sell_usdt
            resp = p2p.get_listing_for_currency(
                currency=currency.code,
                trade_type="SELL",
                **sell_filters
            )

            data = p2p.extract_relevant_data(resp)
            best_match = data[0] 
            CurrencyExchangeConditions.objects.create(
                currency=currency,
                price=best_match.get("price", ''),
                publisher_name=best_match.get("nickName", ''),
                opertarion_type_for_usdt=CurrencyExchangeConditions.OperationType.SELL,
                extra_data_listing={
                    "payTimeLimit": best_match.get("payTimeLimit", ''),
                    "minSingleTransAmount": best_match.get("minSingleTransAmount", ''),
                    "maxSingleTransAmount": best_match.get("maxSingleTransAmount", ''),
                    "tradeMethods": best_match.get("tradeMethods", ''),

                },
                extra_data_publisher={"positiveRate":best_match.get("positiveRate", '')}
            )


        self.stdout.write("succefull") 
        


