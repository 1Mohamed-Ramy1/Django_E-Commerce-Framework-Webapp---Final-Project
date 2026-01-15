"""
Coupon and promotional code models for discount management.

Supports percentage and fixed-amount discounts with usage limits,
expiration dates, and minimum order requirements.
"""
from django.db import models
from django.utils import timezone


class Coupon(models.Model):
    """Discount code with flexible discount types and validation rules."""

    PERCENTAGE = "percentage"
    FIXED = "fixed"

    DISCOUNT_TYPE_CHOICES = [
        (PERCENTAGE, "Percentage"),
        (FIXED, "Fixed Amount"),
    ]

    code = models.CharField(
        max_length=50, unique=True, db_index=True, help_text="Unique coupon code"
    )
    discount_type = models.CharField(
        max_length=20, choices=DISCOUNT_TYPE_CHOICES, help_text="Type of discount"
    )
    value = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Discount value (% or amount)"
    )
    min_order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Minimum order total to apply coupon",
    )

    max_uses = models.PositiveIntegerField(help_text="Total redemptions allowed")
    used_count = models.PositiveIntegerField(
        default=0, help_text="Number of times coupon has been used"
    )

    is_active = models.BooleanField(default=True, db_index=True)
    expires_at = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-expires_at"]

    def __str__(self):
        return self.code

    def is_valid(self, order_total):
        """Check if coupon can be applied given conditions."""
        if not self.is_active:
            return False
        if self.used_count >= self.max_uses:
            return False
        if timezone.now() > self.expires_at:
            return False
        if order_total < self.min_order_total:
            return False
        return True

    def calculate_discount(self, order_total):
        """Calculate discount amount for given order total."""
        if self.discount_type == self.PERCENTAGE:
            return (order_total * self.value) / 100
        return min(self.value, order_total)
