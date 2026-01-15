"""Django admin configuration for coupons.

Customizes the admin interface for managing discount codes.
"""
from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """Admin interface for discount coupons."""

    list_display = [
        "code",
        "discount_type",
        "value",
        "used_count",
        "max_uses",
        "is_active",
        "expires_at",
    ]
    list_filter = ["discount_type", "is_active", "expires_at"]
    search_fields = ["code"]
    readonly_fields = ["used_count", "created_at"]
    ordering = ["-expires_at"]

    fieldsets = (
        (
            "Coupon Code",
            {"fields": ("code", "discount_type", "value")},
        ),
        (
            "Usage Limits",
            {
                "fields": (
                    "max_uses",
                    "used_count",
                    "min_order_total",
                )
            },
        ),
        (
            "Status",
            {"fields": ("is_active", "expires_at")},
        ),
        ("System", {"fields": ("created_at",), "classes": ("collapse",)}),
    )