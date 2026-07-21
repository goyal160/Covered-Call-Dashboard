from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response

from .models import CashHolding, CoveredCall
from .serializers import (
    CashHoldingSerializer,
    CoveredCallSerializer,
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
# CASH HOLDINGS
# ==========================================================

class CashHoldingViewSet(viewsets.ModelViewSet):

    authentication_classes = [
        TokenAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    queryset = CashHolding.objects.all()

    serializer_class = CashHoldingSerializer


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

    def get_queryset(self):

        queryset = CoveredCall.objects.all()

        status_filter = self.request.query_params.get("status")

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        holding = self.request.query_params.get("holding")

        if holding:
            queryset = queryset.filter(script_name=holding)

        return queryset.order_by("-trade_date")