from django.contrib import admin

from .models import CashHolding, CoveredCall


@admin.register(CashHolding)
class CashHoldingAdmin(admin.ModelAdmin):

    list_display = (
        "script_name",
        "buy_average",
        "current_price",
        "quantity",
        "investment",
        "current_value",
        "gain_loss",
        "charges",
    )

    search_fields = (
        "script_name",
    )

    ordering = (
        "script_name",
    )

    readonly_fields = (
        "investment",
        "current_value",
        "gain_loss",
    )


@admin.register(CoveredCall)
class CoveredCallAdmin(admin.ModelAdmin):

    list_display = (
        "holding",
        "trade_date",
        "expiry_date",
        "strike",
        "sell_average",
        "buy_average",
        "quantity",
        "status",
        "net_profit",
    )

    search_fields = (
        "holding__script_name",
    )

    list_filter = (
        "status",
        "expiry_date",
        "trade_date",
    )

    ordering = (
        "-trade_date",
    )

    readonly_fields = (
        "net_profit",
    )