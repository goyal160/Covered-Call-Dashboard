from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CashHoldingViewSet,
    CoveredCallViewSet,
    login_view,
    logout_view,
)

router = DefaultRouter()

router.register(
    "cash-holdings",
    CashHoldingViewSet,
    basename="cash-holdings",
)

router.register(
    "covered-calls",
    CoveredCallViewSet,
    basename="covered-calls",
)

urlpatterns = [

    # =====================================================
    # Authentication
    # =====================================================

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

    # =====================================================
    # API
    # =====================================================

    path(
        "",
        include(router.urls),
    ),

]