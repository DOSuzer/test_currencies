from rest_framework import serializers
from rest_framework.serializers import ValidationError


class RatesSerializer(serializers.Serializer):
    """Сериализатор для валютных пар."""
    RUB = serializers.FloatField(required=True)


class USDCurrencyRatesSerializer(serializers.Serializer):
    """Сериализатор для курсов валют относительно USD."""
    rates = RatesSerializer(required=True)
    base = serializers.CharField(required=True)

    def validate_base(self, value):
        if value != 'USD':
            raise ValidationError(f'Неверная валютная пара: {value}')
        return value
