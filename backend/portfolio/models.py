from decimal import Decimal

from django.db import models

from django.utils import timezone


class CashHolding(models.Model):

    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("CLOSED", "Closed"),
    ]

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

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="OPEN",
    )

    close_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    close_date = models.DateField(
        null=True,
        blank=True,
    )

    realized_gain = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
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

    opening_charges = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    closing_charges = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
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
            self.closing_charges = Decimal("0.00")
            self.net_profit = Decimal("0.00")

        else:

            gross_profit = (
                self.sell_average -
                self.buy_average
            ) * self.quantity

            total_charges = (
                self.opening_charges
                + self.closing_charges
            )

            self.net_profit = (
                gross_profit
                - total_charges
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.holding.script_name} | "
            f"{self.strike} | "
            f"{self.expiry_date}"
        )


class CashTransaction(models.Model):

    TRANSACTION_TYPES = [

        ("INITIAL", "Initial Capital"),
        ("DEPOSIT", "Deposit"),
        ("WITHDRAW", "Withdrawal"),

        ("BUY", "Buy Holding"),
        ("SELL", "Sell Holding"),

        ("PREMIUM", "Option Premium"),
        ("BUYBACK", "Option Buyback"),

        ("ADJUSTMENT", "Adjustment"),
    ]

    transaction_date = models.DateField(
        default=timezone.localdate,
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    remarks = models.CharField(
        max_length=250,
        blank=True,
    )

    holding = models.ForeignKey(
        CashHolding,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cash_transactions",
    )

    running_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    notes = models.CharField(
        max_length=250,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-transaction_date",
            "-id",
        ]

        indexes = [
            models.Index(fields=["transaction_date"]),
            models.Index(fields=["transaction_type"]),
        ]

    def __str__(self):

        return (
            f"{self.transaction_date} - "
            f"{self.transaction_type} - "
            f"₹{self.amount}"
        )

    @property
    def signed_amount(self):

        if self.transaction_type in [
            "BUY",
            "WITHDRAW",
            "BUYBACK",
        ]:
            return -self.amount

        return self.amount