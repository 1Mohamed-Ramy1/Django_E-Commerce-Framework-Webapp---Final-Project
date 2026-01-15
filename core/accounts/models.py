"""
User account models for profile management, authentication, and transactions.

Extends Django's User model with additional profile data, balance tracking,
and password reset functionality.
"""
import random
from django.db import models
from django.contrib.auth.models import User


class PasswordReset(models.Model):
    """Secure password reset with 6-digit activation code."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activation_code = models.CharField(
        max_length=6, unique=True, editable=False, db_index=True,
        help_text="6-digit activation code sent to user's email"
    )
    created_when = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_when"]

    def save(self, *args, **kwargs):
        if not self.activation_code:
            # Generate unique 6-digit code
            while True:
                code = str(random.randint(100000, 999999))
                if not PasswordReset.objects.filter(activation_code=code).exists():
                    self.activation_code = code
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Password reset for {self.user.username} (Code: {self.activation_code})"


class Profile(models.Model):
    """Extended user profile with contact, payment, and loyalty information."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    # Country selected by the user (stored as plain name)
    country = models.CharField(max_length=100, blank=True, default='Egypt', help_text='Country of residence')

    image = models.ImageField(
        upload_to="profiles/", default="profiles/default.png"
    )

    warning = models.BooleanField(
        default=False, help_text="Account warning flag for violations"
    )
    blocked = models.BooleanField(
        default=False, help_text="Account blocked flag prevents login"
    )

    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, help_text="Account wallet balance"
    )
    total_spent = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, help_text="Lifetime spending total"
    )
    last_purchase = models.DateTimeField(
        null=True, blank=True, help_text="Last order date"
    )

    loyalty_points = models.IntegerField(
        default=0, help_text="Loyalty program points"
    )
    points = models.IntegerField(default=0, help_text="Redeemable points")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.user.username


class BalanceTransaction(models.Model):
    """Record of wallet balance changes (deposits, payments, refunds)."""

    TRANSACTION_TYPES = [
        ("deposit", "Deposit"),
        ("payment", "Payment"),
        ("refund", "Refund"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="balance_transactions"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    reference = models.CharField(
        max_length=100, blank=True, help_text="Reference to order/transaction ID"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.amount}"
