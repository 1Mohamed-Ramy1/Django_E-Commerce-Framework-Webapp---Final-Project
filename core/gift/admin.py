"""Django admin configuration for gifts and rewards.

Customizes the admin interface for managing gift items and redemptions.
"""
from django.contrib import admin
from .models import Gift, GiftRedemption


@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    """Admin interface for redeemable gifts."""

    list_display = ["name", "points_cost", "stock_quantity", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "description"]
    list_editable = ["points_cost", "stock_quantity", "is_active"]
    readonly_fields = ["uid", "created_at"]
    ordering = ["points_cost", "name"]

    fieldsets = (
        ("Gift Information", {"fields": ("uid", "name", "description", "image")}),
        (
            "Pricing & Stock",
            {"fields": ("points_cost", "stock_quantity", "is_active")},
        ),
        ("Metadata", {"fields": ("created_at",), "classes": ("collapse",)}),
    )


@admin.register(GiftRedemption)
class GiftRedemptionAdmin(admin.ModelAdmin):
    """Admin interface for gift redemptions."""

    list_display = ["user", "gift", "points_spent", "status", "redeemed_at"]
    list_filter = ["status", "redeemed_at"]
    search_fields = ["user__username", "gift__name", "tracking_number"]
    readonly_fields = ["uid", "redeemed_at"]
    ordering = ["-redeemed_at"]
    readonly_fields = ['uid', 'redeemed_at', 'points_spent']
    list_editable = ['status']
    
    fieldsets = (
        ('Redemption Info', {
            'fields': ('uid', 'user', 'gift', 'points_spent', 'redeemed_at')
        }),
        ('Fulfillment', {
            'fields': ('status', 'tracking_number', 'notes')
        }),
    )
