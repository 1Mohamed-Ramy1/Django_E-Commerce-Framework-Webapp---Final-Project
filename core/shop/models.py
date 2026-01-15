"""
Shop models for product catalog, inventory, and cart management.

This module defines models for product categories, product details, sizing,
and shopping cart functionality.
"""
from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Size options for apparel products
SIZE_CHOICES = [
    ("XS", "XS"),
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("XXL", "XXL"),
]


class Category(models.Model):
    """Product category for organizing the catalog."""

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        """Auto-generate slug from category name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_active_discount(self):
        """
        Get the highest active discount event for this category.
        Returns tuple: (discount_percentage, event) or (0, None)
        """
        from events.models import Event
        from django.utils import timezone
        
        active_events = Event.objects.filter(
            is_active=True,
            status='live',
            categories=self,
            event_date__lte=timezone.now()
        ).order_by('-discount_percentage')
        
        if active_events.exists():
            event = active_events.first()
            return event.discount_percentage, event
        
        return 0, None
    
    def has_active_discount(self):
        """Check if category has an active discount."""
        discount_percentage, _ = self.get_active_discount()
        return discount_percentage > 0
    
    @property
    def discount_badge(self):
        """Get discount badge info for display."""
        discount_percentage, event = self.get_active_discount()
        return {
            'active': discount_percentage > 0,
            'percentage': discount_percentage,
            'event': event
        }


class Subcategory(models.Model):
    """Subcategory nested under a main category for finer organization."""

    category = models.ForeignKey(
        Category, related_name="subcategories", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Subcategories"
        ordering = ["name"]
        unique_together = ("category", "slug")

    def save(self, *args, **kwargs):
        """Auto-generate slug from subcategory name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Product(models.Model):
    """Product catalog with pricing, inventory, and category links."""

    legacy_id = models.IntegerField(
        null=True, blank=True, db_index=True, help_text="Legacy product ID for data migration"
    )
    name = models.CharField(max_length=200)
    category_ref = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Primary category assignment",
    )
    subcategory = models.ForeignKey(
        Subcategory,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Optional subcategory assignment",
    )
    category = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Legacy category field (deprecated, use category_ref)",
    )

    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)

    image = models.URLField(max_length=500, blank=True, null=True, help_text="Product image URL")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    
    def get_active_event_discount(self):
        """
        Get the highest active event discount for this product's category.
        Returns tuple: (discount_percentage, event) or (0, None)
        """
        if not self.category_ref:
            return 0, None
        
        from events.models import Event
        from django.utils import timezone
        
        # Get active events that include this product's category
        active_events = Event.objects.filter(
            is_active=True,
            status='live',
            categories=self.category_ref,
            event_date__lte=timezone.now()
        ).order_by('-discount_percentage')
        
        if active_events.exists():
            event = active_events.first()
            return event.discount_percentage, event
        
        return 0, None
    
    def get_discounted_price(self):
        """
        Calculate the discounted price if an active event applies to this product.
        Returns the discounted price or original price if no discount.
        """
        discount_percentage, event = self.get_active_event_discount()
        
        if discount_percentage > 0:
            from decimal import Decimal
            discount_amount = self.price * Decimal(discount_percentage / 100)
            return self.price - discount_amount
        
        return self.price
    
    def has_active_discount(self):
        """Check if product has an active discount from an event."""
        discount_percentage, _ = self.get_active_event_discount()
        return discount_percentage > 0
    
    @property
    def discount_info(self):
        """Get discount information as dict for templates."""
        discount_percentage, event = self.get_active_event_discount()
        return {
            'has_discount': discount_percentage > 0,
            'percentage': discount_percentage,
            'original_price': self.price,
            'discounted_price': self.get_discounted_price(),
            'event': event,
            'savings': self.price - self.get_discounted_price() if discount_percentage > 0 else 0
        }


class ProductSize(models.Model):
    """Size variants available for a product with individual stock tracking."""

    product = models.ForeignKey(
        Product, related_name="sizes", on_delete=models.CASCADE
    )
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ("product", "size")
        verbose_name_plural = "Product Sizes"

    def __str__(self):
        return f"{self.product.name} - {self.size}"


class Cart(models.Model):
    """Shopping cart associated with a user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="carts"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def total_price(self):
        """Calculate total price of all items in cart."""
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    """Individual item in a shopping cart with size and quantity selection."""

    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product", "size")
        verbose_name_plural = "Cart Items"

    def subtotal(self):
        """Calculate subtotal for this cart item using discounted price if available."""
        # Use discounted price if product has active discount
        price = self.product.get_discounted_price()
        return price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.size}) x{self.quantity}"
