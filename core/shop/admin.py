"""
Django admin configuration for shop models.

Customizes the admin interface for managing products, categories, and cart items.
"""
from django.contrib import admin
from .models import Category, Subcategory, Product, ProductSize, Cart, CartItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for product categories."""

    list_display = ["name", "slug", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """Admin interface for product subcategories."""

    list_display = ["name", "category", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["category"]
    search_fields = ["name", "category__name"]
    ordering = ["category", "name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for products with enhanced category display."""

    list_display = ["name", "get_category", "subcategory", "price", "stock"]
    list_filter = ["category_ref", "subcategory", "created_at"]
    search_fields = ["name", "category_ref__name"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "category_ref", "subcategory", "created_at")},
        ),
        (
            "Description",
            {"fields": ("short_description", "description")},
        ),
        (
            "Pricing & Stock",
            {"fields": ("price", "stock")},
        ),
        (
            "Media",
            {"fields": ("image",)},
        ),
        (
            "Legacy",
            {"fields": ("legacy_id", "category"), "classes": ("collapse",)},
        ),
    )

    def get_category(self, obj):
        """Display category name with fallback to legacy text field."""
        if obj.category_ref:
            return obj.category_ref.name
        return obj.category or "Uncategorized"

    get_category.short_description = "Category"


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    """Admin interface for product sizes and variants."""

    list_display = ["product", "size", "quantity"]
    list_filter = ["size", "product__category_ref"]
    search_fields = ["product__name"]
    ordering = ["product", "size"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin interface for shopping carts."""

    list_display = ["id", "user", "created_at", "get_item_count"]
    list_filter = ["created_at"]
    search_fields = ["user__username"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_item_count(self, obj):
        """Display number of items in cart."""
        return obj.items.count()

    get_item_count.short_description = "Items"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin interface for individual cart items."""

    list_display = ["cart", "product", "size", "quantity", "get_subtotal"]
    list_filter = ["size", "cart__user"]
    search_fields = ["product__name", "cart__user__username"]
    ordering = ["cart", "product"]

    def get_subtotal(self, obj):
        """Display calculated subtotal for the item."""
        return f"${obj.subtotal()}"

    get_subtotal.short_description = "Subtotal"

