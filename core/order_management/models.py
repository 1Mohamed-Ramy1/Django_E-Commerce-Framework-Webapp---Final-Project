"""
Order management models for tracking customer orders and line items.

Handles order lifecycle, pricing calculations, delivery tracking, and
payment status.
"""
from decimal import Decimal
from django.db import models
from django.conf import settings
from shop.models import Product


SIZE_CHOICES = [
    ("XS", "XS"),
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("XXL", "XXL"),
]


class Order(models.Model):
    """Customer order with status tracking and payment management."""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    delivery_address = models.TextField(
        blank=True, null=True, help_text="Shipping address"
    )
    delivery_fee = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Sum of all order items",
    )
    final_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Total amount + delivery fee",
    )
    paid_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )

    payment_method = models.CharField(max_length=50, blank=True)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default="pending", db_index=True
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["status", "-created_at"]),
        ]

    def __str__(self):
        return f"Order #{self.id} - {self.user}"

    def recalc_totals(self):
        """Recalculate totals from order items and persist changes."""
        total = Decimal("0.00")
        for item in self.items.all():
            # Ensure item has a recorded price
            if item.price is None:
                item.price = (
                    item.product.price if item.product else Decimal("0.00")
                )
                item.save()
            total += item.price * item.quantity

        self.total_amount = total
        self.final_total = total + (self.delivery_fee or Decimal("0.00"))
        self.save()
        return self.total_amount


class OrderItem(models.Model):
    """Individual line item in an order with product and pricing info."""

    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(
        max_length=50, blank=True, help_text="Size variant selected"
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Price at time of order",
    )

    class Meta:
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.product} x{self.quantity}"

    def subtotal(self):
        """Calculate line item subtotal."""
        return (self.price or Decimal("0.00")) * self.quantity
