from decimal import Decimal

from django.db import models


class CashHolding(models.Model):

    script_name = models.CharField(
        max_length=50,
        unique=True
    )

    buy_average = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    current_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField()

    charges = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    class Meta:
        ordering = ["script_name"]

    @property
    def investment(self):
        if self.buy_average is None or self.quantity is None:
            return 0
        return self.buy_average * self.quantity

    @property
    def current_value(self):
        if self.current_price is None or self.quantity is None:
            return 0
        return self.current_price * self.quantity

    @property
    def gain_loss(self):
        if (
            self.buy_average is None
            or self.current_price is None
            or self.quantity is None
        ):
            return 0

        return (
            self.current_price -
            self.buy_average
        ) * self.quantity

    def __str__(self):
        return self.script_name


class CoveredCall(models.Model):

    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("CLOSED", "Closed"),
    ]

    holding = models.ForeignKey(
        CashHolding,
        on_delete=models.CASCADE,
        related_name="covered_calls"
    )

    trade_date = models.DateField()

    expiry_date = models.DateField()

    strike = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    sell_average = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    buy_average = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    quantity = models.PositiveIntegerField()

    charges = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    close_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="OPEN"
    )

    net_profit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    class Meta:
        ordering = [
            "-trade_date",
            "holding__script_name"
        ]

    def save(self, *args, **kwargs):

        if self.status == "OPEN":

            self.buy_average = Decimal("0.00")
            self.close_date = None
            self.net_profit = Decimal("0.00")

        else:

            self.net_profit = (
                (
                    self.sell_average -
                    self.buy_average
                ) * self.quantity
            ) - self.charges

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.holding.script_name} | "
            f"{self.strike} | "
            f"{self.expiry_date}"
        )