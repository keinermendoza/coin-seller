from decimal import Decimal, ROUND_HALF_DOWN
from django.utils import timezone as tz
from django.core.management import call_command 

from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    GenericAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import serializers, status
from p2p.models import (
    Currency,
    CurrencyExchangeConditions,
    FiatExchangePair,
    FiatExchangePairRate,
    ImageCoordinates,
    UserFiatPreferences,
    TradeRequest,
    Exchange
)

from .serializers import (
    CalculatorBuyRateSerializer,
    CalculatorSellRateSerializer,
    ImageCoordinatesSerializer,
    TradeRequestSerializer,
    ExchangeCreateAssociateSerializer,
    ExchangeSerializer
)

class CalculatorRatesApiView(APIView):
    """
    uses current user fiat preferences for return data to live buy/sell calculator feature  
    """
    permission_classes = [permissions.AllowAny]
    def get(self, request, *args, **kwargs):
        user = request.user
        user_fiat_pairs_in_sell = FiatExchangePair.objects.user_suscribed_sell_side(user)
        user_fiat_pairs_in_buy = FiatExchangePair.objects.user_suscribed_buy_side(user)
        
        serilaizer_sell = CalculatorSellRateSerializer(user_fiat_pairs_in_sell, many=True)
        serilaizer_buy = CalculatorBuyRateSerializer(user_fiat_pairs_in_buy, many=True)

        return Response(
            {"now": tz.now(), "buy": serilaizer_buy.data, "sell": serilaizer_sell.data}, status=status.HTTP_200_OK
        )

class FiatPairBasicDicstSerializer(serializers.Serializer):
    """
    map fields from a dict
    """
    id = serializers.IntegerField(source="pair__id")
    side = serializers.CharField(source='side_operation')
    currencyFrom = serializers.CharField(source='pair__currency_from__code')
    currencyTo = serializers.CharField(source='pair__currency_to__code')
    currencyFromSymbol = serializers.CharField(source='pair__currency_from__symbol')
    currencyToSymbol = serializers.CharField(source="pair__currency_to__symbol")
            

class TradeRequestView(ListCreateAPIView):
    serializer_class = TradeRequestSerializer

    def get_queryset(self):
        return TradeRequest.objects.user_suscribed(self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        fiat_pair_list = request.user.fiat_preferences.values(
            "side_operation",
            "pair__id",
            "pair__currency_from__code",
            "pair__currency_to__code",
            "pair__currency_from__symbol",
            "pair__currency_to__symbol",

        )
        fiat_pair_serializer = FiatPairBasicDicstSerializer(fiat_pair_list, many=True)
        data = {
            "fiat_suscriptions": fiat_pair_serializer.data,
            "results": response.data
        }
        return Response(data, status=status.HTTP_200_OK)        

class ExchangeUpdateAPIView(RetrieveUpdateAPIView):
    """
    Updates exchange operation for mistaken registry
    """
    serializer_class = ExchangeSerializer
    queryset = Exchange.objects.all()
    
class ExchangeAPIView(APIView):
    """
    creates an exchange operation and 
    returns the corresponding TradeRquest instance updated
    """
    def post(self, request, *args, **kwargs):
        exchange_serializer = ExchangeCreateAssociateSerializer(data=request.data)
        exchange_serializer.is_valid(raise_exception=True)
        exchange_serializer.save(registered_by=self.request.user)
        trade = TradeRequest.objects.get(id=request.data.get('trade_request_id'))
        trade_serializer = TradeRequestSerializer(trade)
        print(trade_serializer.data)
        return Response(trade_serializer.data, status=status.HTTP_201_CREATED)
    
class RatesAutoUpdateAction(APIView):
    def post(self, request, *args, **kwargs):
        fiat_pairs = FiatExchangePair.objects.all()
        for fiat_pair in fiat_pairs:
            fiat_pair.create_rate()
        return Response(status=status.HTTP_201_CREATED)

class ImageCoordinatesView(APIView):
    def get(self, request, *args, **kwargs):
        images = ImageCoordinates.objects.all()
        serializer = ImageCoordinatesSerializer(images, many=True)
        return Response(serializer.data)

class FiatExchangePairListAPIView(ListAPIView):
    """
    List FiatExchangePair for use to fetch specific FiatExchangePair's market data
    """
    queryset = FiatExchangePair.objects.all()

    def get_serializer_class(self):
        class JustInTimeSerializer(serializers.ModelSerializer):
            currency_from = serializers.StringRelatedField()
            currency_to = serializers.StringRelatedField()

            class Meta:
                model = FiatExchangePair
                fields = ["id", "slug", "currency_from", "currency_to"]
        return JustInTimeSerializer

class FiatExchangePairMarketAPIView(RetrieveAPIView):
    """
    displays specific FiatExchangePair's market data
    """
    queryset = FiatExchangePair.objects.all()
    lookup_field = "slug"

    def post(self, request, *args, **kwargs):
        pair = self.get_object()
        if new_rate := request.data.get('newrate'):
            pair.create_rate(new_rate)

            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


    def get_serializer_class(self):
        class JustInTimeSerializer(serializers.ModelSerializer):
            currency_from = serializers.StringRelatedField()
            currency_to = serializers.StringRelatedField()
            market_rate = serializers.SerializerMethodField()
            market_time = serializers.SerializerMethodField()
            current_rate = serializers.SerializerMethodField()

            sugested_rate = serializers.SerializerMethodField()
            # optimum_margin_expected = serializers.DecimalField(max_digits=10, decimal_places=3, coerce_to_string=False)

            class Meta:
                model = FiatExchangePair
                fields = "__all__"

            def get_market_rate(self, obj):
                return obj.get_market_rate()
            
            def get_sugested_rate(self, obj):
                if optimum := obj.get_market_rate_plus_optimum_margin():
                    return Decimal(optimum.quantize(
                        Decimal("0.0000"), rounding=ROUND_HALF_DOWN
                    ))

            def get_market_time(self, obj):
                buy, sell = obj._get_last_currency_exchange_conditions_pair_buy_sell()
                if buy and sell:
                    return {"buy_time":buy.created, "sell_time":sell.created}

            def get_current_rate(self,obj):
                return obj.last_rate.rate
        
        return JustInTimeSerializer

class ReadMarketConditions(APIView):
    def post(self, request, *args, **kwargs):
        call_command("retrive_data_from_binance")
        return Response(status=status.HTTP_200_OK)
    


    
# class MarketAndCurrencyPairConditionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = 

# class MarketAndCurrencyPairConditionsAPIView(APIView):
#     """
#     shows all trade conditions for currency
#     """
#     ## recuperar todos los pares de cambios
#     for pair in FiatExchangePair.objects.all():
        
#         last_buys = CurrencyExchangeConditions.objects.filter(
#             currency=pair.currency_from,
#             conditions__operation_type=CurrencyExchangeConditions.OperationType.BUY
#         )[:10]

#         last_sells = CurrencyExchangeConditions.objects.filter(
#             currency=pair.currency_from,
#             conditions__operation_type=CurrencyExchangeConditions.OperationType.SELL
#         )[:10]
    
    ### recuperar precio de mercado para el cambio con campos:
    # get_market_rate_plus_optimum_margin
    # get_market_rate
        ### - hora del precio calculado

    # pass
    # def get(self, request, *args, **kwargs):
        
        # FiatExchangePair.