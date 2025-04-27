from decimal import Decimal, ROUND_HALF_UP
from django.test import TestCase
from datetime import timedelta
from django.utils import timezone as tz
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

from p2p.models import (
    Currency,
    CurrencyOperationPreferences,
    CurrencyExchangeConditions,
    FiatExchangePair,
    FiatExchangePairRate,
    UserFiatPreferences,
    TradeRequest,
    Exchange,
)


def create_currencies():
    bolivar = Currency.objects.create(name="Bolivar", symbol="Bs", code="VES")

    real = Currency.objects.create(name="Real", symbol="R$", code="BRL")

    # craeting bolivar filters
    bolivar_filters = {"payTypes": ["PagoMovil"], "transAmount": 2000}

    CurrencyOperationPreferences.objects.create(
        currency=bolivar,
        filter_for_buy_usdt=bolivar_filters,
        filter_for_sell_usdt=bolivar_filters,
    )

    # craeting real filters
    real_filters = {"payTypes": ["PIX"], "transAmount": 100}

    CurrencyOperationPreferences.objects.create(
        currency=real,
        filter_for_buy_usdt=real_filters,
        filter_for_sell_usdt=real_filters,
    )


def create_fiat_exchange_pairs():
    bolivar = Currency.objects.get(name="Bolivar")
    real = Currency.objects.get(name="Real")

    FiatExchangePair.objects.create(
        currency_from=bolivar,
        currency_to=real,
        optimum_margin_expected=4.5,
        minimum_margin_expected=2,
        maximum_margin_limit=6.5,
    )

    FiatExchangePair.objects.create(
        currency_from=real,
        currency_to=bolivar,
        optimum_margin_expected=4.5,
        minimum_margin_expected=2,
        maximum_margin_limit=6.5,
    )


def helper_create_currency_conditions(to_create):
    for obj in to_create:
        CurrencyExchangeConditions.objects.create(**obj)


def mock_currency_conditions_for_ves_to_brl():
    bolivar = Currency.objects.get(name="Bolivar")
    real = Currency.objects.get(name="Real")

    obj_to_create = [
        {
            "currency": bolivar,
            "price": 101150,
            "created": tz.now() - timedelta(minutes=3),
            "operation_type": CurrencyExchangeConditions.OperationType.BUY,
        },
        {
            "currency": bolivar,
            "price": 103550,
            "created": tz.now() - timedelta(minutes=2),
            "operation_type": CurrencyExchangeConditions.OperationType.BUY,
        },
        {
            "currency": bolivar,
            "price": 104250,
            "created": tz.now() - timedelta(minutes=1),
            "operation_type": CurrencyExchangeConditions.OperationType.BUY,
        },
        {
            "currency": real,
            "price": 5.569,
            "created": tz.now() - timedelta(minutes=3),
            "operation_type": CurrencyExchangeConditions.OperationType.SELL,
        },
        {
            "currency": real,
            "price": 5.842,
            "created": tz.now() - timedelta(minutes=2),
            "operation_type": CurrencyExchangeConditions.OperationType.SELL,
        },
        {
            "currency": real,
            "price": 5.570,
            "created": tz.now() - timedelta(minutes=1),
            "operation_type": CurrencyExchangeConditions.OperationType.SELL,
        },
    ]

    helper_create_currency_conditions(obj_to_create)


def create_users():
    User.objects.create(username="pepe", email="pepe@gmail.com", password="12345678")
    User.objects.create(username="paco", email="paco@gmail.com", password="12345678")

    User.objects.create(
        username="carlos", email="carlos@gmail.com", password="12345678"
    )

    User.objects.create(
        username="antonio", email="antonio@gmail.com", password="12345678"
    )


def create_users_and_fiat_preferences():
    create_users()

    pepe = User.objects.get(username="pepe")
    paco = User.objects.get(username="paco")

    brl_ves = FiatExchangePair.objects.get(slug="brl_ves")
    ves_brl = FiatExchangePair.objects.get(slug="ves_brl")

    UserFiatPreferences.objects.create(
        user=pepe,
        pair=brl_ves,
        side_operation=UserFiatPreferences.ExchangeSideOperation.BUY,
    )

    UserFiatPreferences.objects.create(
        user=paco,
        pair=brl_ves,
        side_operation=UserFiatPreferences.ExchangeSideOperation.BUY,
    )

    UserFiatPreferences.objects.create(
        user=paco,
        pair=ves_brl,
        side_operation=UserFiatPreferences.ExchangeSideOperation.SELL,
    )


class FiatExchangePairTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_currencies()
        create_fiat_exchange_pairs()
        mock_currency_conditions_for_ves_to_brl()

    def test_fiat_exchange_pair_uses_last_available_currency_exchange_condition(self):
        ves_brl = FiatExchangePair.objects.get(
            currency_from__name="Bolivar", currency_to__name="Real"
        )

        ves_brl.create_rate()
        ves_brl.create_rate()
        ves_brl.create_rate()

        last_rate = FiatExchangePairRate.objects.order_by("-created").first()
        self.assertEqual(ves_brl.last_rate.created, last_rate.created)

    # def test_get_market_rate_uses_last_available_prices(self):
    #     ves_brl = FiatExchangePair.objects.get(
    #         currency_from__name="Bolivar",
    #         currency_to__name="Real"
    #     )
    #     market_rate = ves_brl.get_market_rate()

    #     last_buy_ves = CurrencyExchangeConditions.objects.filter(
    #         operation_type=CurrencyExchangeConditions.OperationType.BUY,
    #         currency__name="Bolivar"
    #     ).order_by("-created").first()

    #     last_sell_brl = CurrencyExchangeConditions.objects.filter(
    #         operation_type=CurrencyExchangeConditions.OperationType.SELL,
    #         currency__name="Real"
    #     ).order_by("-created").first()

    #     self.assertEqual(last_buy_ves.price, Decimal(104250).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP))
    #     self.assertEqual(last_sell_brl.price, Decimal(5.570).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP))
    #     self.assertEqual(market_rate, last_sell_brl.price / last_buy_ves.price)

    def test_user_suscribed_query_method(self):
        create_users_and_fiat_preferences()

        # ves_brl = FiatExchangePair.objects.get(slug="ves_brl")
        paco = User.objects.get(username="paco")

        buy = FiatExchangePair.objects.user_suscribed_buy_side(paco)
        sell = FiatExchangePair.objects.user_suscribed_sell_side(paco)


        print("buy", buy)
        print("sell", sell)



class UserFiatPreferencesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_currencies()
        create_fiat_exchange_pairs()
        create_users()

    def test_user_can_have_multiple_preferences(self):
        pepe = User.objects.get(username="pepe")
        ves_brl = FiatExchangePair.objects.get(slug="ves_brl")
        brl_ves = FiatExchangePair.objects.get(slug="brl_ves")

        pepe_suscribes_ves_brl = UserFiatPreferences.objects.create(
            user=pepe,
            pair=ves_brl,
            side_operation=UserFiatPreferences.ExchangeSideOperation.BUY,
        )
        pepe_suscribes_brl_ves = UserFiatPreferences.objects.create(
            user=pepe,
            pair=brl_ves,
            side_operation=UserFiatPreferences.ExchangeSideOperation.BUY,
        )

        self.assertIsInstance(pepe_suscribes_ves_brl, UserFiatPreferences)
        self.assertIsInstance(pepe_suscribes_brl_ves, UserFiatPreferences)

    def test_multiple_users_can_have_same_preferences(self):
        pepe = User.objects.get(username="pepe")
        paco = User.objects.get(username="paco")

        brl_ves = FiatExchangePair.objects.get(slug="brl_ves")
        pepe_suscribes_brl_ves = UserFiatPreferences.objects.create(
            user=pepe,
            pair=brl_ves,
            side_operation=UserFiatPreferences.ExchangeSideOperation.BUY,
        )
        paco_suscribes_brl_ves = UserFiatPreferences.objects.create(
            user=paco,
            pair=brl_ves,
            side_operation=UserFiatPreferences.ExchangeSideOperation.BUY,
        )

        self.assertIsInstance(paco_suscribes_brl_ves, UserFiatPreferences)
        self.assertIsInstance(pepe_suscribes_brl_ves, UserFiatPreferences)

    def test_user_cannot_have_multiple_preferences_in_same_pair(self):
        paco = User.objects.get(username="paco")
        brl_ves = FiatExchangePair.objects.get(slug="brl_ves")
        UserFiatPreferences.objects.create(
            user=paco,
            pair=brl_ves,
            side_operation=UserFiatPreferences.ExchangeSideOperation.BUY,
        )
        with self.assertRaises(ValidationError):
            UserFiatPreferences.objects.create(
                user=paco,
                pair=brl_ves,
                side_operation=UserFiatPreferences.ExchangeSideOperation.BUY,
            )



class TradeRequestTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_currencies()
        create_fiat_exchange_pairs()
        create_users_and_fiat_preferences()

    def test_trade_request_minimum_required_data(self):
        brl_ves = FiatExchangePair.objects.get(slug="brl_ves")
        req = TradeRequest.objects.create(requested_amount=100, pair=brl_ves)
        self.assertIsInstance(req, TradeRequest)

    def test_user_suscribed_manager_method(slef):
        # brl_ves = FiatExchangePair.objects.get(slug="brl_ves")
        ves_brl = FiatExchangePair.objects.get(slug="ves_brl")

        t100 = TradeRequest.objects.create(
            requested_amount=100,
            pair=ves_brl,
            status=TradeRequest.TradeOperationStatus.COMPLETED,
        )
        t50 = TradeRequest.objects.create(requested_amount=50, pair=ves_brl)
        t2 = TradeRequest.objects.create(requested_amount=2, pair=ves_brl)

        paco = User.objects.get(username="paco")
        pepe = User.objects.get(username="pepe")
        antonio = User.objects.get(username="antonio")

        paco_open = TradeRequest.objects.open().user_suscribed(paco)
        pepe_open = TradeRequest.objects.open().user_suscribed(pepe)
        antonio_open = TradeRequest.objects.open().user_suscribed(antonio)

    def test_one_side_ready_for_user_manager_method(slef):
        pass
