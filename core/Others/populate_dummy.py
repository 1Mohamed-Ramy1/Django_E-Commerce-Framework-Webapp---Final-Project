"""
Populate database with dummy data for development and testing.

This script creates sample users, blog posts, shop products, events, and orders
to provide a realistic development environment without manual data entry.
"""
import os
import django
import random
from datetime import timedelta

# Django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.utils import timezone
from django.contrib.auth import get_user_model

# Import core models
from blog.models import Post as BlogPost, Category as BlogCategory
from events.models import Event
from weather.models import SearchHistory

# Import shop models with graceful fallback for compatibility
User = get_user_model()

try:
    from shop.models import Product as ShopProduct, Order as ShopOrder, OrderItem as ShopOrderItem
except Exception:
    ShopProduct = None
    ShopOrder = None
    ShopOrderItem = None

print("=== Running populate_dummy.py ===")

# ============================================================================
# USER CREATION
# ============================================================================

print("\nAdding/updating dummy users...")

# Create regular test users
for i in range(1, 6):
    username = f"user{i}"
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": f"{username}@example.com"}
    )
    if created:
        user.set_password("password123")
        user.save()
        print(f"  [+] Created user: {username}")
    else:
        print(f"  [*] User exists: {username}")

# Create admin user
admin, created = User.objects.get_or_create(
    username="admin",
    defaults={"email": "admin@example.com"}
)
if created:
    admin.set_password("adminpass")
    try:
        admin.is_staff = True
        admin.is_superuser = True
    except AttributeError:
        pass
    admin.save()
    print("  [+] Created admin user")
else:
    print("  [*] Admin user exists")

# ============================================================================
# BLOG CONTENT
# ============================================================================

print("\nAdding dummy blog categories...")
blog_categories = []
for cat_name in ["Tech", "Lifestyle", "News"]:
    cat, created = BlogCategory.objects.get_or_create(
        name=cat_name,
        defaults={"description": f"Category for {cat_name}"}
    )
    blog_categories.append(cat)
    if created:
        print(f"  [+] Created category: {cat_name}")
    else:
        print(f"  [*] Category exists: {cat_name}")

print("\nAdding dummy blog posts...")
for i in range(1, 6):
    title = f"Blog Post {i}"
    BlogPost.objects.get_or_create(
        title=title,
        defaults={
            "content": f"This is the content for {title}. Lorem ipsum dolor sit amet.",
            "category": random.choice(blog_categories),
            "image": ""
        }
    )
print("  [+] Blog posts created")

# ============================================================================
# SHOP PRODUCTS
# ============================================================================

if ShopProduct is not None:
    print("\nAdding dummy shop products...")
    try:
        from shop.models import Category as ShopCategory

        base_categories = ["Men", "Women", "Kids", "Unisex"]
        cat_objs = []
        
        # Create or fetch product categories
        for cname in base_categories:
            cat, _ = ShopCategory.objects.get_or_create(name=cname)
            cat_objs.append(cat)

        # Create sample products linked to categories
        for i in range(1, 9):
            name = f"Shop Product {i}"
            chosen_category = random.choice(cat_objs)
            ShopProduct.objects.get_or_create(
                name=name,
                defaults={
                    "category_ref": chosen_category,
                    "category": chosen_category.name,
                    "price": random.randint(20, 300),
                    "image": ""
                }
            )
        print("  [+] Shop products created with category links")
        
    except Exception as e:
        # Fallback for model compatibility issues
        print(f"  [!] Category linking failed ({type(e).__name__}), using legacy category field")
        base_categories = ["Men", "Women", "Kids", "Unisex"]
        for i in range(1, 9):
            name = f"Shop Product {i}"
            ShopProduct.objects.get_or_create(
                name=name,
                defaults={
                    "category": random.choice(base_categories),
                    "price": random.randint(20, 300),
                    "image": ""
                }
            )
        print("  [+] Shop products created (legacy mode)")
else:
    print("\n[!] Shop app not available - skipping products")

# ============================================================================
# EVENTS
# ============================================================================

print("\nAdding dummy events...")
for i in range(1, 4):
    name = f"Event {i}"
    Event.objects.get_or_create(
        name=name,
        defaults={
            "event_date": timezone.now() + timedelta(days=i),
            "status": "running"
        }
    )
print("  [+] Events created")

# ============================================================================
# WEATHER DATA
# ============================================================================

print("\nAdding dummy weather search history...")
cities = ["Cairo", "Alexandria", "Giza"]
for city in cities:
    try:
        SearchHistory.objects.get_or_create(
            city_name=city,
            defaults={
                "temperature": round(random.uniform(15.0, 35.0), 1)
            }
        )
    except Exception as e:
        print(f"  [!] Warning: Could not create weather entry for {city}: {type(e).__name__}")
print("  [+] Weather history processed")

# ============================================================================
# SAMPLE ORDERS
# ============================================================================

if ShopOrder is not None and ShopOrderItem is not None and ShopProduct is not None:
    print("\nAdding sample order...")
    
    # Get a regular (non-admin) user for the order
    user = None
    if hasattr(User, "is_superuser"):
        user = User.objects.filter(is_superuser=False).first()
    if not user:
        user = User.objects.first()
    
    product = ShopProduct.objects.first()
    
    if user and product:
        order, created = ShopOrder.objects.get_or_create(
            user=user,
            defaults={
                "payment_method": "CashOnDelivery",
                "date": timezone.now()
            }
        )
        
        # Create order item only for newly created orders
        if created:
            try:
                ShopOrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=1,
                    price_at_order=getattr(product, "price", 0),
                    size="M"
                )
            except TypeError:
                # Fallback for different model schema
                try:
                    ShopOrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=1
                    )
                except Exception as e:
                    print(f"  [!] Could not create order item: {e}")
        
        print("  [+] Sample order created or already exists")
    else:
        print("  [!] Could not create order: missing user or product")
else:
    print("\n[!] Shop order models not available - skipping orders")

print("\n=== populate_dummy.py finished ===\n")
