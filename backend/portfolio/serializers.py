from rest_framework import serializers

from .models import CashHolding, CoveredCall


class CashHoldingSerializer(serializers.ModelSerializer):

    investment = serializers.ReadOnlyField()
    current_value = serializers.ReadOnlyField()
    gain_loss = serializers.ReadOnlyField()

    class Meta:
        model = CashHolding
        fields = [
            "id",
            "script_name",
            "buy_average",
            "current_price",
            "quantity",
            "charges",
            "investment",
            "current_value",
            "gain_loss",
        ]


class CoveredCallSerializer(serializers.ModelSerializer):

    holding_name = serializers.CharField(
        source="holding.script_name",
        read_only=True
    )

    class Meta:
        model = CoveredCall
        fields = [
            "id",
            "holding",
            "holding_name",
            "trade_date",
            "expiry_date",
            "strike",
            "sell_average",
            "buy_average",
            "quantity",
            "charges",
            "status",
            "close_date",
            "net_profit",
        ]

        read_only_fields = [
            "net_profit",
            "holding_name",
        ]