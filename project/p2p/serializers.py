from rest_framework import serializers, status
from p2p.models import (
    Currency,
    FiatExchangePair,
    FiatExchangePairRate,
    ImageCoordinates,
    TradeRequest,
    Exchange

)

class ExchangeSerializer(serializers.ModelSerializer):
    registeredBy = serializers.SerializerMethodField()
    class Meta:
        fields = ["id", "amount", "price", "registeredBy", "created"]  
        model = Exchange  

    def get_registeredBy(self, obj):
        return obj.registered_by.username
    
class TradeRequestSerializer(serializers.ModelSerializer):
    status_text = serializers.SerializerMethodField()
    exchange_buy = ExchangeSerializer(read_only=True)
    exchange_sell =  ExchangeSerializer(read_only=True)
    class Meta:
        fields = "__all__"
        model = TradeRequest

    def get_status_text(self, obj):
        return obj.get_status_display()
    
class ExchangeCreateAssociateSerializer(serializers.ModelSerializer):
    """
    perform creation of Exchange operation 
    and associates to corresponding TradeRequest instance
    """
    trade_request_id = serializers.IntegerField()
    class Meta:
        model = Exchange
        fields = "__all__"

    def create(self, validated_data):
        side = validated_data.get('side_operation')
        relation = {
            Exchange.ExchangeSideOperation.BUY: "exchange_buy",
            Exchange.ExchangeSideOperation.SELL:"exchange_sell"
        }
        trade_id = validated_data.pop('trade_request_id')
        exchange = Exchange.objects.create(**validated_data)
        trade = TradeRequest.objects.get(id=trade_id)
        setattr(trade, relation[side], exchange)
        trade.save()

        return exchange
    
### for Calculator exchanges functionality
class FiatExchangeRateSellSerializer(serializers.ModelSerializer):
    """
    uses last available rate for display equilibry SELL price (where there is no profit nor lost)
    for more info check p2p.models.FiatExchangePairRate.sell_price_limit 
    """
    sell_price_limit = serializers.SerializerMethodField()

    class Meta:
        fields = ["created", "rate", "sell_price_limit"]
        model = FiatExchangePairRate

    def get_sell_price_limit(self, obj):
        return obj.sell_price_limit()

class FiatExchangeRateBuySerializer(serializers.ModelSerializer):
    """
    uses last available rate for display equilibry BUY price (where there is no profit nor lost)
    for more info check p2p.models.FiatExchangePairRate.buy_price_limit 
    """
    buy_price_limit = serializers.SerializerMethodField()

    class Meta:
        fields = ["created", "rate", "buy_price_limit"]
        model = FiatExchangePairRate

    def get_buy_price_limit(self, obj):
        return obj.buy_price_limit()

class CurrencySerializer(serializers.ModelSerializer):
    """
    displays info about Currency Instances
    """
    class Meta:
        exclude = ["created", "edited"]
        model = Currency

class CalculatorBaseRateSerializer(serializers.Serializer):
    """
    Base serializer for display Currency data related to particular FiatExchangePair
    """
    currencyFrom = CurrencySerializer(source="currency_from")
    currencyTo = CurrencySerializer(source="currency_to")

class CalculatorBuyRateSerializer(CalculatorBaseRateSerializer):
    """
    Displays FiatExchangePair data + info about last BUY rate point of equilbrium
    """
    rateInfo = serializers.SerializerMethodField()

    def get_rateInfo(self, obj):
        last_rate = obj.last_rate
        return FiatExchangeRateBuySerializer(last_rate).data
    
class CalculatorSellRateSerializer(CalculatorBaseRateSerializer):
    """
    Displays FiatExchangePair data + info about last SELL rate point of equilbrium
    """
    rateInfo = serializers.SerializerMethodField()

    def get_rateInfo(self, obj):
        last_rate = obj.last_rate
        return FiatExchangeRateSellSerializer(last_rate).data

### for Image download functionality

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
        slugs = [p["slug"] for p in rep.get("points", [])]

        # Obtener los valores actualizados del modelo TipoCambio
        tipos = FiatExchangePair.objects.filter(slug__in=slugs)
        ####
        tipo_map = {t.slug: str(t.valor) for t in tipos}

        # Reemplazar el texto si el slug corresponde a un tipo de cambio
        for point in rep["points"]:
            slug = point.get("slug")
            if slug in tipo_map:
                point["text"] = tipo_map[slug]

        return rep
