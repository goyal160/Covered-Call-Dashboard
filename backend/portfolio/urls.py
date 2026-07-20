from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CashHoldingViewSet,
    CoveredCallViewSet,
)

router = DefaultRouter()

router.register(
    r"cash-holdings",
    CashHoldingViewSet,
    basename="cash-holdings",
)

router.register(
    r"covered-calls",
    CoveredCallViewSet,
    basename="covered-calls",
)

urlpatterns = [
    path("", include(router.urls)),
]