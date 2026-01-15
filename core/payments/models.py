"""
Payment models for tracking payment methods and transaction status.

Handles payment confirmation, method selection, and order completion
workflow.
"""
from django.db import models
from django.utils import timezone
from order_management.models import Order


class Payment(models.Model):
    """Payment record linked to an order."""

    METHOD_CHOICES = [
        ("cash", "Cash on Delivery"),
        ("visa", "Visa Card"),
    ]

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment"
    )
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    is_paid = models.BooleanField(default=False, db_index=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-paid_at"]

    def confirm(self):
        """Mark payment as complete and update order status."""
        self.is_paid = True
        self.paid_at = timezone.now()
        self.order.status = "paid"
        self.order.save()
        self.save()

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.get_method_display()}"
