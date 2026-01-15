"""
Gift and rewards models for loyalty program and gift redemption.

Manages gift catalog, user redemptions, and reward tracking with
status and shipment tracking.
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Gift(models.Model):
    """Redeemable gift item in the loyalty rewards program."""

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    points_cost = models.IntegerField(help_text="Loyalty points required to redeem")
    image = models.ImageField(upload_to="gifts/", null=True, blank=True)
    stock_quantity = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["points_cost", "name"]
        verbose_name_plural = "Gifts"

    def __str__(self):
        return f"{self.name} ({self.points_cost} points)"


class GiftRedemption(models.Model):
    """Record of a user redeeming a gift item."""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("shipped", "Shipped"),
    ]

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="gift_redemptions"
    )
    gift = models.ForeignKey(Gift, on_delete=models.PROTECT, related_name="redemptions")
    points_spent = models.IntegerField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", db_index=True
    )
    tracking_number = models.CharField(
        max_length=100, blank=True, null=True, help_text="Shipment tracking number"
    )
    notes = models.TextField(blank=True, help_text="Admin notes on redemption")
    redeemed_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-redeemed_at"]
        verbose_name_plural = "Gift Redemptions"

    def __str__(self):
        return f"{self.user.username} - {self.gift.name}"
