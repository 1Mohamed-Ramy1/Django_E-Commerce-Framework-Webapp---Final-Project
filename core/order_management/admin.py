"""Django admin configuration for orders.

Customizes the admin interface for managing orders and line items.
"""
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline admin for order items within orders."""

    model = OrderItem
    extra = 0
    readonly_fields = ["product", "quantity", "size", "price"]
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for customer orders."""

    list_display = [
        "id",
        "user",
        "status",
        "total_amount",
        "final_total",
        "payment_method",
        "created_at",
    ]
    list_filter = ["status", "payment_method", "created_at"]
    search_fields = ["user__username", "user__email", "delivery_address"]
    readonly_fields = ["total_amount", "final_total", "created_at"]
    ordering = ["-created_at"]
    inlines = [OrderItemInline]

    fieldsets = (
        (
            "Order Information",
            {"fields": ("user", "status", "created_at")},
        ),
        (
            "Delivery",
            {"fields": ("delivery_address", "delivery_fee")},
        ),
        (
            "Pricing",
            {"fields": ("total_amount", "final_total", "paid_amount")},
        ),
        (
            "Payment",
            {"fields": ("payment_method",)},
        ),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for individual order items."""

    list_display = ["order", "product", "size", "quantity", "price"]
    list_filter = ["order__created_at", "size"]
    search_fields = ["order__id", "product__name"]
    readonly_fields = ["order", "product", "quantity", "size", "price"]
    can_delete = False
    ordering = ["-order__created_at"]