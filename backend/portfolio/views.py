from rest_framework import filters, viewsets

from .models import CashHolding, CoveredCall
from .serializers import (
    CashHoldingSerializer,
    CoveredCallSerializer,
)


class CashHoldingViewSet(viewsets.ModelViewSet):

    serializer_class = CashHoldingSerializer

    queryset = CashHolding.objects.all().order_by("script_name")

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "script_name",
    ]

    ordering_fields = [
        "script_name",
        "buy_average",
        "current_price",
        "quantity",
    ]

    ordering = [
        "script_name",
    ]


class CoveredCallViewSet(viewsets.ModelViewSet):

    serializer_class = CoveredCallSerializer

    queryset = (
        CoveredCall.objects
        .select_related("holding")
        .all()
        .order_by("-trade_date")
    )

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "holding__script_name",
        "strike",
    ]

    ordering_fields = [
        "trade_date",
        "expiry_date",
        "strike",
        "status",
        "net_profit",
    ]

    ordering = [
        "-trade_date",
    ]

    def get_queryset(self):

        queryset = (
            CoveredCall.objects
            .select_related("holding")
            .all()
        )

        status = self.request.query_params.get("status")

        if status:
            queryset = queryset.filter(
                status=status.upper()
            )

        return queryset.order_by("-trade_date")