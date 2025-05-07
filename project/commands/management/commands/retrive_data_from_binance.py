import requests as rq
from django.core.management.base import BaseCommand, CommandError
from p2p.models import Currency, CurrencyExchangeConditions

from binance_client import p2p


class Command(BaseCommand):
    help = "retrives data from binance and save it in db"

    def handle(self, *args, **options):
        currencies = Currency.objects.all()

        for currency in currencies:

            # buy petition
            buy_filters = currency.operation_preferences.filter_for_buy_usdt
            resp = p2p.get_listing_for_currency(
                currency=currency.code, trade_type="BUY", **buy_filters
            )

            if resp["success"]:
                self.stdout.write(
                    f"data for BUY USDT using {currency.name} retrived suceffully"
                )

                data = p2p.extract_relevant_data(resp)
                second_best_match = data[1]
                CurrencyExchangeConditions.objects.create(
                    currency=currency,
                    price=second_best_match.get("price", ""),
                    publisher_name=second_best_match.get("nickName", ""),
                    operation_type=CurrencyExchangeConditions.OperationType.BUY,
                    extra_data_listing={
                        "payTimeLimit": second_best_match.get("payTimeLimit", ""),
                        "minSingleTransAmount": second_best_match.get(
                            "minSingleTransAmount", ""
                        ),
                        "maxSingleTransAmount": second_best_match.get(
                            "maxSingleTransAmount", ""
                        ),
                        "tradeMethods": second_best_match.get("tradeMethods", ""),
                    },
                    extra_data_publisher={
                        "positiveRate": second_best_match.get("positiveRate", "")
                    },
                )
            else:
                self.stderr.write("solicitud no exitosa.")  # NEW
                self.stderr.write(resp)  # NEW

            # sell petition
            sell_filters = currency.operation_preferences.filter_for_sell_usdt
            resp = p2p.get_listing_for_currency(
                currency=currency.code, trade_type="SELL", **sell_filters
            )

            if resp["success"]:
                self.stdout.write(
                    f"data for SELL USDT to {currency.name} retrived suceffully"
                )

                data = p2p.extract_relevant_data(resp)
                second_best_match = data[1]
                CurrencyExchangeConditions.objects.create(
                    currency=currency,
                    price=second_best_match.get("price", ""),
                    publisher_name=second_best_match.get("nickName", ""),
                    operation_type=CurrencyExchangeConditions.OperationType.SELL,
                    extra_data_listing={
                        "payTimeLimit": second_best_match.get("payTimeLimit", ""),
                        "minSingleTransAmount": second_best_match.get(
                            "minSingleTransAmount", ""
                        ),
                        "maxSingleTransAmount": second_best_match.get(
                            "maxSingleTransAmount", ""
                        ),
                        "tradeMethods": second_best_match.get("tradeMethods", ""),
                    },
                    extra_data_publisher={
                        "positiveRate": second_best_match.get("positiveRate", "")
                    },
                )
            else:
                self.stderr.write("solicitud no exitosa.")  # NEW
                self.stderr.write(resp)  # NEW
