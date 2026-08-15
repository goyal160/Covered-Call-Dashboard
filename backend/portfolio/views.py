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
    Dividend,
)

from .serializers import (
    CashHoldingSerializer,
    CoveredCallSerializer,
    CashTransactionSerializer,
    DividendSerializer,
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
            "DIVIDEND",
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

    def perform_update(self, serializer):

        old = self.get_object()

        # -----------------------------
        # Store old values
        # -----------------------------
        old_quantity = old.quantity
        old_buy_average = old.buy_average
        old_status = old.status

        old_investment = (
            old_buy_average *
            old_quantity
        )

        # -----------------------------
        # Save edited holding
        # -----------------------------
        holding = serializer.save()

        # -----------------------------
        # Only OPEN holdings affect cash
        # -----------------------------
        if old_status != "OPEN" or holding.status != "OPEN":
            return

        new_investment = (
            holding.buy_average *
            holding.quantity
        )

        difference = new_investment - old_investment

        if difference == 0:
            return

        # ---------------------------------------
        # More investment -> BUY adjustment
        # ---------------------------------------
        if difference > 0:

            CashTransaction.objects.create(

                transaction_date=timezone.localdate(),

                transaction_type="BUY",

                amount=difference,

                holding=holding,

                remarks=f"Adjustment BUY - {holding.script_name}",

            )

        # ---------------------------------------
        # Reduced investment -> SELL adjustment
        # ---------------------------------------
        else:

            CashTransaction.objects.create(

                transaction_date=timezone.localdate(),

                transaction_type="SELL",

                amount=abs(difference),

                holding=holding,

                remarks=f"Adjustment SELL - {holding.script_name}",

            )

        update_running_balance()


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
# DIVIDENDS
# ==========================================================

class DividendViewSet(viewsets.ModelViewSet):

    authentication_classes = [
        TokenAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = DividendSerializer

    queryset = Dividend.objects.all().order_by(
        "-dividend_date",
        "-id",
    )

    def get_queryset(self):

        queryset = Dividend.objects.all().order_by(
            "-dividend_date",
            "-id",
        )

        holding = self.request.query_params.get(
            "holding"
        )

        if holding:

            queryset = queryset.filter(
                holding__script_name=holding
            )

        return queryset

    def perform_create(self, serializer):

        dividend = serializer.save()

        CashTransaction.objects.create(

            transaction_date=dividend.dividend_date,

            transaction_type="DIVIDEND",

            amount=dividend.amount,

            holding=dividend.holding,

            remarks=(
                f"Dividend received - "
                f"{dividend.holding.script_name}"
            ),

        )

        update_running_balance()

    def perform_update(self, serializer):

        old = self.get_object()

        old_amount = old.amount
        old_date = old.dividend_date
        old_holding = old.holding

        dividend = serializer.save()

        # --------------------------------------------------
        # Update corresponding cash transaction
        # --------------------------------------------------

        transaction = CashTransaction.objects.filter(
            transaction_type="DIVIDEND",
            holding=old_holding,
            transaction_date=old_date,
            amount=old_amount,
            remarks__startswith="Dividend received -",
        ).order_by("-id").first()

        if transaction:

            transaction.transaction_date = (
                dividend.dividend_date
            )

            transaction.amount = dividend.amount

            transaction.holding = dividend.holding

            transaction.remarks = (
                f"Dividend received - "
                f"{dividend.holding.script_name}"
            )

            transaction.save()

        update_running_balance()

    def perform_destroy(self, instance):

        # --------------------------------------------------
        # Remove corresponding cash transaction
        # --------------------------------------------------

        transaction = CashTransaction.objects.filter(
            transaction_type="DIVIDEND",
            holding=instance.holding,
            transaction_date=instance.dividend_date,
            amount=instance.amount,
            remarks__startswith="Dividend received -",
        ).order_by("-id").first()

        if transaction:
            transaction.delete()

        instance.delete()

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