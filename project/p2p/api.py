from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import serializers, status
from p2p.models import (
    Currency,
    FiatExchangePair,
    FiatExchangePairRate,
    ImageCoordinates,
)

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["created", "edited"]
        model = Currency



class SellDataSerializer(serializers.ModelSerializer):
    sell_price_limit = serializers.SerializerMethodField()
    
    class Meta:
        fields = ["created", "rate", "sell_price_limit"]
        model = FiatExchangePairRate
    
    def get_sell_price_limit(self, obj):
        return obj.sell_price_limit()
    

class BuyDataSerializer(serializers.ModelSerializer):
    buy_price_limit = serializers.SerializerMethodField()
    
    class Meta:
        fields = ["created", "rate", "buy_price_limit"]
        model = FiatExchangePairRate
    
    def get_buy_price_limit(self, obj):
        return obj.buy_price_limit()

    

class BuyDataView(APIView):
    def get(self, request, *args, **kwargs):
        ves_brl = FiatExchangePair.objects.get(
            currency_from__name="Bolivar",
            currency_to__name="Real"
        )
        rate_ves_brl = ves_brl.last_rate
        currencyFrom = CurrencySerializer(ves_brl.currency_from)
        currencyTo = CurrencySerializer(ves_brl.currency_to)
        rateInfo = BuyDataSerializer(rate_ves_brl)

        return Response({
            "currencyFrom":currencyFrom.data,
            "currencyTo": currencyTo.data,
            **rateInfo.data
        }, status=status.HTTP_200_OK)

class SellDataView(APIView):
    def get(self, request, *args, **kwargs):
        brl_ves = FiatExchangePair.objects.get(
            currency_from__name="Real",
            currency_to__name="Bolivar"
        )
        rate_brl_ves = brl_ves.last_rate
        currencyFrom = CurrencySerializer(brl_ves.currency_from)
        currencyTo = CurrencySerializer(brl_ves.currency_to)
        rateInfo = SellDataSerializer(rate_brl_ves)

        return Response({
            "currencyFrom":currencyFrom.data,
            "currencyTo": currencyTo.data,
            **rateInfo.data
        }, status=status.HTTP_200_OK)
    

class LayoutImageCoordinateSerializer(serializers.Serializer):
    type = serializers.SlugField()
    width = serializers.IntegerField(min_value=100)
    height = serializers.IntegerField(min_value=100)
    image_base = serializers.CharField(max_length=200) 

class CoordinatePairSerializer(serializers.Serializer):
    x = serializers.IntegerField(min_value=0)
    y = serializers.IntegerField(min_value=0)

class PointCoordinateSerializer(serializers.Serializer):
    has_fk = serializers.BooleanField()
    slug = serializers.SlugField()
    text = serializers.CharField(max_length=40)
    position = CoordinatePairSerializer()

class ImageCoordinatesSerializer(serializers.ModelSerializer):
    points = PointCoordinateSerializer(many=True)
    layout = LayoutImageCoordinateSerializer()
    class Meta:
        model = ImageCoordinates
        fields = ["name", "points", "font_size", "layout"]


    def to_representation(self, instance):
        rep = super().to_representation(instance)

        # Extraer los slugs de todos los puntos
        slugs = [p['slug'] for p in rep.get('points', [])]

        # Obtener los valores actualizados del modelo TipoCambio
        tipos = FiatExchangePair.objects.filter(slug__in=slugs)
        ####
        tipo_map = {t.slug: str(t.valor) for t in tipos}

        # Reemplazar el texto si el slug corresponde a un tipo de cambio
        for point in rep['points']:
            slug = point.get('slug')
            if slug in tipo_map:
                point['text'] = tipo_map[slug]

        return rep
    

class ImageCoordinatesView(APIView):
    def get(self, request, *args, **kwargs):
        images = ImageCoordinates.objects.all()
        serializer = ImageCoordinatesSerializer(images, many=True)
        return Response(serializer.data)