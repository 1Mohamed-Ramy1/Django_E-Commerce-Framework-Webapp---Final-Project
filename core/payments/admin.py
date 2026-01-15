"""Django admin configuration for payments.

Customizes the admin interface for managing payment records.
"""
from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin interface for order payments."""

    list_display = ["id", "order", "method", "is_paid", "paid_at"]
    list_filter = ["method", "is_paid"]
    search_fields = ["order__id", "order__user__username"]
    readonly_fields = ["paid_at"]
    ordering = ["-paid_at"]
