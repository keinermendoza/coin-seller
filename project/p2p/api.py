from django.utils import timezone as tz
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    CreateAPIView
)

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import serializers, status
from p2p.models import (
    Currency,
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
    ExchangeCreateAssociateSerializer
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
        )
        fiat_pair_serializer = FiatPairBasicDicstSerializer(fiat_pair_list, many=True)
        data = {
            "fiat_suscriptions": fiat_pair_serializer.data,
            "results": response.data
        }
        return Response(data, status=status.HTTP_200_OK)        



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
