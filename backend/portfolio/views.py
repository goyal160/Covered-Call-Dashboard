from django.contrib.auth import authenticate
from django.utils.dateparse import parse_date
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from decimal import Decimal
from django.utils import timezone

from rest_framework.decorators import (
    action,
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response

from .models import (
    CashHolding,
    CoveredCall,
    CashTransaction,
)

from .serializers import (
    CashHoldingSerializer,
    CoveredCallSerializer,
    CashTransactionSerializer,
)


# ==========================================================
# LOGIN
# ==========================================================

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(
        username=username,
        password=password,
    )

    if user is None:

        return Response(
            {
                "success": False,
                "message": "Invalid username or password.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token, created = Token.objects.get_or_create(
        user=user
    )

    return Response(
        {
            "success": True,
            "token": token.key,
            "username": user.username,
        }
    )


# ==========================================================
# LOGOUT
# ==========================================================

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):

    request.user.auth_token.delete()

    return Response(
        {
            "success": True,
            "message": "Logged out successfully.",
        }
    )


# ==========================================================
# CASH LEDGER INITIALIZATION
# ==========================================================

def update_running_balance():

    balance = Decimal("0.00")

    transactions = CashTransaction.objects.order_by(
        "transaction_date",
        "id",
    )

    for tx in transactions:

        if tx.transaction_type in (
            "INITIAL",
            "DEPOSIT",
            "SELL",
            "PREMIUM",
        ):

            balance += tx.amount

        else:

            balance -= tx.amount

        tx.running_balance = balance

        tx.save(
            update_fields=["running_balance"]
        )


def initialize_cash_ledger():

    if CashTransaction.objects.exists():
        return


# ==========================================================
# CASH HOLDINGS
# ==========================================================

class CashHoldingViewSet(viewsets.ModelViewSet):

    authentication_classes = [
        TokenAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    queryset = CashHolding.objects.all().order_by("-id")

    serializer_class = CashHoldingSerializer

    def get_queryset(self):

        queryset = CashHolding.objects.all().order_by("-id")

        status = self.request.query_params.get("status")

        if status:

            queryset = queryset.filter(
                status=status.upper()
            )

        return queryset


    def perform_create(self, serializer):

        holding = serializer.save()

        investment = (
            holding.buy_average
            * holding.quantity
        )

        CashTransaction.objects.create(

            transaction_date=timezone.now().date(),

            transaction_type="BUY",

            amount=investment,

            holding=holding,

            remarks=f"Bought {holding.script_name}",

        )

        update_running_balance()


    @action(detail=True, methods=["post"])
    def close(self, request, pk=None):

        holding = self.get_object()

        if holding.status == "CLOSED":
            return Response(
                {"detail": "Holding already closed."},
                status=400,
            )

        sell_price = Decimal(
            request.data.get(
                "sell_price",
                holding.current_price,
            )
        )

        closing_charges = Decimal(
            request.data.get(
                "charges",
                0,
            )
        )

        close_date = request.data.get("close_date")

        if close_date:
            close_date = parse_date(close_date)
        else:
            close_date = timezone.localdate()

        sale_value = sell_price * holding.quantity

        investment = (
            holding.buy_average
            * holding.quantity
        )

        realized_gain = (
            sale_value
            - investment
            - holding.charges
            - closing_charges
        )

        holding.close_price = sell_price
        holding.close_date = close_date
        holding.realized_gain = realized_gain
        holding.status = "CLOSED"
        holding.charges += closing_charges

        holding.save()

        CashTransaction.objects.create(

            transaction_date=holding.close_date,

            transaction_type="SELL",

            amount=sale_value,

            holding=holding,

            remarks=f"Sold {holding.script_name}",

        )

        update_running_balance()

        serializer = self.get_serializer(holding)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

# ==========================================================
# COVERED CALLS
# ==========================================================

class CoveredCallViewSet(viewsets.ModelViewSet):

    authentication_classes = [
        TokenAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = CoveredCallSerializer

    queryset = CoveredCall.objects.all().order_by(
        "-trade_date",
        "-id",
    )

    def get_queryset(self):

        queryset = CoveredCall.objects.all().order_by(
            "-trade_date",
            "-id",
        )

        status_filter = self.request.query_params.get("status")

        if status_filter:

            queryset = queryset.filter(
                status=status_filter.upper()
            )

        holding = self.request.query_params.get("holding")

        if holding:

            queryset = queryset.filter(
                holding__script_name=holding
            )

        return queryset

    def perform_create(self, serializer):

        call = serializer.save()

        premium_received = (
            call.sell_average
            * call.quantity
        )

        CashTransaction.objects.create(

            transaction_date=call.trade_date,

            transaction_type="PREMIUM",

            amount=premium_received,

            holding=call.holding,

            remarks=(
                f"Premium received - "
                f"{call.holding.script_name}"
            ),

        )

        update_running_balance()

    def perform_update(self, serializer):

        old = self.get_object()

        was_open = old.status == "OPEN"

        call = serializer.save()

        if was_open and call.status == "CLOSED":

            buyback_cost = (

                call.buy_average
                * call.quantity

            ) + call.closing_charges

            CashTransaction.objects.create(

                transaction_date=call.close_date,

                transaction_type="BUYBACK",

                amount=buyback_cost,

                holding=call.holding,

                remarks=(
                    f"Buyback - "
                    f"{call.holding.script_name}"
                ),

            )

            update_running_balance()

# ==========================================================
# PORTFOLIO CASH VIEW
# ==========================================================

class CashTransactionViewSet(viewsets.ModelViewSet):

    authentication_classes = [
        TokenAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = CashTransactionSerializer

    queryset = CashTransaction.objects.all().order_by(
        "-transaction_date",
        "-id",
    )

    def list(self, request, *args, **kwargs):

        initialize_cash_ledger()

        return super().list(
            request,
            *args,
            **kwargs,
        )

    def perform_create(self, serializer):

        transaction = serializer.save()

        update_running_balance()


    def perform_update(self, serializer):

        serializer.save()

        update_running_balance()


    def perform_destroy(self, instance):

        instance.delete()

        update_running_balance()