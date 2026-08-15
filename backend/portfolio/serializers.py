from rest_framework import serializers

from .models import (
    CashHolding,
    CoveredCall,
    CashTransaction,
    Dividend,
)


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

            "status",
            "close_price",
            "close_date",
            "realized_gain",
        ]

        read_only_fields = [
            "investment",
            "current_value",
            "gain_loss",
            "realized_gain",
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
            "opening_charges",
            "closing_charges",
            "status",
            "close_date",
            "net_profit",
        ]

        read_only_fields = [
            "net_profit",
            "holding_name",
        ]


class DividendSerializer(serializers.ModelSerializer):

    holding_name = serializers.CharField(
        source="holding.script_name",
        read_only=True,
    )

    class Meta:

        model = Dividend

        fields = [
            "id",
            "holding",
            "holding_name",
            "dividend_date",
            "amount",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "holding_name",
            "created_at",
            "updated_at",
        ]

class CashTransactionSerializer(serializers.ModelSerializer):

    holding_name = serializers.CharField(
        source="holding.script_name",
        read_only=True,
    )

    class Meta:

        model = CashTransaction

        fields = [
            "id",
            "transaction_date",
            "transaction_type",
            "amount",
            "remarks",
            "notes",
            "holding",
            "holding_name",
            "running_balance",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "running_balance",
            "created_at",
            "updated_at",
            "holding_name",
        ]