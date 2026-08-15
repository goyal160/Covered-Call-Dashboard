from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CashHoldingViewSet,
    CoveredCallViewSet,
    CashTransactionViewSet,
    DividendViewSet,
    login_view,
    logout_view,
)


router = DefaultRouter()


# ==========================================================
# CASH HOLDINGS
# ==========================================================

router.register(
    "cash-holdings",
    CashHoldingViewSet,
    basename="cash-holdings",
)


# ==========================================================
# COVERED CALLS
# ==========================================================

router.register(
    "covered-calls",
    CoveredCallViewSet,
    basename="covered-calls",
)


# ==========================================================
# DIVIDENDS
# ==========================================================

router.register(
    "dividends",
    DividendViewSet,
    basename="dividends",
)


# ==========================================================
# CASH TRANSACTIONS
# ==========================================================

router.register(
    "cash-transactions",
    CashTransactionViewSet,
    basename="cash-transactions",
)


urlpatterns = [

    # ======================================================
    # AUTHENTICATION
    # ======================================================

    path(
        "auth/login/",
        login_view,
        name="login",
    ),

    path(
        "auth/logout/",
        logout_view,
        name="logout",
    ),

    # ======================================================
    # API
    # ======================================================

    path(
        "",
        include(router.urls),
    ),
]