from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from decimal import Decimal

from .models import Cart, CartItem, Product, ProductSize, Category, Subcategory
from order_management.models import Order, OrderItem
from payments.models import Payment


# -------------------------------------------------
# Helpers
# -------------------------------------------------
def get_user_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


# -------------------------------------------------
# Shop Pages (Templates – OLD but still supported)
# -------------------------------------------------
def shop_home(request):
    from blog.models import Post
    from django.db.models import Q
    
    products = Product.objects.order_by('?')[:48]
    # Get 4 random published posts, excluding any with "Test" or "test" in title
    recent_blogs = Post.objects.filter(
        is_published=True
    ).exclude(
        Q(title__icontains='test')
    ).order_by('?')[:4]
    
    return render(request, 'shop/shop_home.html', {
        'products': products,
        'recent_blogs': recent_blogs,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Only show sizes for clothing products
    is_clothing = product.category_ref and 'Clothing' in product.category_ref.name
    sizes = product.sizes.all() if is_clothing else []
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'sizes': sizes,
        'is_clothing': is_clothing
    })


# -------------------------------------------------
# Cart (DB Based – NEW)
# -------------------------------------------------
@login_required
def add_to_cart(request, product_id):
    size = request.POST.get('size', None)
    quantity = int(request.POST.get('quantity', 1))

    product = get_object_or_404(Product, id=product_id)
    
    # Check if it's a clothing product
    is_clothing = product.category_ref and 'Clothing' in product.category_ref.name
    
    # For clothing products, size is required
    if is_clothing and not size:
        messages.error(request, 'Please select a size')
        return redirect('shop:product_detail', pk=product_id)
    
    if is_clothing:
        # For clothing: check ProductSize inventory
        try:
            product_size = ProductSize.objects.get(product=product, size=size)
        except ProductSize.DoesNotExist:
            messages.error(request, f'Size {size} is not available for this product')
            return redirect('shop:product_detail', pk=product_id)

        available = int(product_size.quantity)

        cart = get_user_cart(request.user)
        item, _ = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            defaults={'quantity': 0}
        )
        current_qty = int(item.quantity)
        desired_total = current_qty + quantity
        if desired_total > available:
            # clamp to available
            item.quantity = max(0, available)
            item.save()
            if available <= current_qty:
                messages.warning(request, f'Max available for size {size} is {available}.')
            else:
                messages.warning(request, f'Quantity adjusted to {available} (max available).')
            return redirect('shop:product_detail', pk=product_id)
    else:
        # For non-clothing products: use general stock
        available = int(product.stock)

        cart = get_user_cart(request.user)
        item, _ = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size='',  # Empty size for non-clothing
            defaults={'quantity': 0}
        )
        current_qty = int(item.quantity)
        desired_total = current_qty + quantity
        if desired_total > available:
            item.quantity = max(0, available)
            item.save()
            if available <= current_qty:
                messages.warning(request, f'Max available quantity is {available}.')
            else:
                messages.warning(request, f'Quantity adjusted to {available} (max available).')
            return redirect('shop:product_detail', pk=product_id)

    item.quantity += quantity
    item.save()

    messages.success(request, f'{product.name} added to cart')
    return redirect('shop:product_detail', pk=product_id)

@login_required
def view_cart(request):
    cart = get_user_cart(request.user)
    items = []

    for item in cart.items.all():
        items.append({
            'id': item.id,
            'product': item.product.name,
            'size': item.size,
            'quantity': item.quantity,
            'price': float(item.product.price),
            'subtotal': float(item.subtotal())
        })

    # compute shipping fee (5%) and final total
    try:
        subtotal = Decimal(str(cart.total_price()))
    except Exception:
        subtotal = Decimal('0.00')
    delivery_fee = (subtotal * Decimal('0.05')).quantize(Decimal('0.01'))
    final_total = (subtotal + delivery_fee).quantize(Decimal('0.01'))

    return render(request, 'shop/cart.html', {
        'items': items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'total': final_total,
    })


@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == 'POST':
        qty = int(request.POST.get('qty', 1))
        if qty <= 0:
            item.delete()
        else:
            # Determine available stock for this item (size-aware)
            available = 0
            if item.size:
                ps = ProductSize.objects.filter(product=item.product, size=item.size).first()
                available = int(ps.quantity) if ps else 0
            else:
                available = int(item.product.stock)

            if qty > available:
                if available <= 0:
                    item.delete()
                    messages.error(request, 'This item is out of stock and was removed from your cart.')
                else:
                    item.quantity = available
                    item.save()
                    messages.warning(request, f'Max available quantity is {available}. Quantity adjusted.')
            else:
                item.quantity = qty
                item.save()

    return redirect('shop:view_cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return JsonResponse({'message': 'Item removed'})


# -------------------------------------------------
# Checkout & Orders
# -------------------------------------------------

@login_required
def checkout_page(request):
    cart = get_user_cart(request.user)
    cart_items = cart.items.all()

    if not cart_items.exists():
        messages.error(request, 'Your cart is empty')
        return redirect('shop:view_cart')

    # Ensure quantities do not exceed available stock just before checkout
    adjusted = False
    for it in list(cart_items):
        available = 0
        if it.size:
            ps = ProductSize.objects.filter(product=it.product, size=it.size).first()
            available = int(ps.quantity) if ps else 0
        else:
            available = int(it.product.stock)

        if it.quantity > available:
            if available <= 0:
                it.delete()
            else:
                it.quantity = available
                it.save()
            adjusted = True

    if adjusted:
        cart_items = cart.items.all()
        if not cart_items.exists():
            messages.error(request, 'Some items are out of stock and were removed.')
            return redirect('shop:view_cart')
        messages.warning(request, 'Some item quantities were adjusted to available stock.')

    # avoid duplicate pending order
    # avoid duplicate pending order: allow new checkout if pending is stale
    pending_qs = Order.objects.filter(user=request.user, status='pending').order_by('-created_at')
    if pending_qs.exists():
        latest = pending_qs.first()
        # if the pending order is recent (within 10 minutes), redirect to its countdown
        try:
            age_seconds = (timezone.now() - latest.created_at).total_seconds()
        except Exception:
            age_seconds = 0

        GRACE_PERIOD = 30  # 30 seconds
        if age_seconds <= GRACE_PERIOD:
            messages.error(request, 'You have a pending order. Complete payment first.')
            return redirect('payments:countdown', order_id=latest.id)
        else:
            # cancel stale pending orders so user can create a new one
            pending_qs.update(status='cancelled')
            messages.info(request, 'An older pending order was cancelled so you can place a new order.')

    # server-side subtotal calculation from cart
    subtotal = Decimal('0.00')
    for it in cart_items:
        # assume CartItem.subtotal() exists, else compute
        try:
            subtotal += Decimal(str(it.subtotal()))
        except Exception:
            subtotal += Decimal(str(it.product.price)) * it.quantity

    delivery_fee = (subtotal * Decimal('0.05')).quantize(Decimal('0.01'))
    final_total = (subtotal + delivery_fee).quantize(Decimal('0.01'))

    if request.method == "POST":
        address = request.POST.get('address')
        method = request.POST.get('payment_method')

        if not address or not address.strip():
            messages.error(request, 'Please enter a delivery address')
            return render(request, 'shop/checkout.html', {
                'cart_items': cart_items,
                'subtotal': subtotal,
                'delivery_fee': delivery_fee,
                'final_total': final_total
            })

        with transaction.atomic():
            # create order with zero totals; will compute from items
            order = Order.objects.create(
                user=request.user,
                delivery_address=address,
                delivery_fee=delivery_fee,
                **({"total_amount": Decimal("0.00")} if hasattr(Order, "total_amount") else {}),
                **({"total_price": Decimal("0.00")} if hasattr(Order, "total_price") else {}),
                **({"final_total": Decimal("0.00")} if hasattr(Order, "final_total") else {}),
            )

            total = Decimal("0.00")
            for ci in cart_items:
                unit_price = Decimal(str(ci.product.price or 0))
                OrderItem.objects.create(
                    order=order,
                    product=ci.product,
                    quantity=ci.quantity,
                    size=ci.size,
                    price=unit_price  # persist unit price
                )
                total += unit_price * ci.quantity

            update_fields = []
            if hasattr(order, "total_amount"):
                order.total_amount = total
                update_fields.append("total_amount")
            if hasattr(order, "total_price"):
                order.total_price = total
                update_fields.append("total_price")
            if hasattr(order, "final_total"):
                order.final_total = total + (order.delivery_fee or Decimal("0.00"))
                update_fields.append("final_total")
            order.save(update_fields=update_fields or None)

            Payment.objects.create(order=order, method=method)
            cart_items.delete()

        return redirect('payments:countdown', order_id=order.id)

    # GET render
    return render(request, 'shop/checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'final_total': final_total
    })


# -------------------------------------------------
# Orders List & Details
# -------------------------------------------------

@login_required
@login_required
def orders_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/orders_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_detail.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    data = []

    for order in orders:
        data.append({
            'order_id': order.id,
            'total': float(order.total_amount()),
            'payment_method': order.payment_method,
            'date': order.created_at
        })

    return JsonResponse({'orders': data})


# -------------------------------------------------
# Admin Product CRUD
# -------------------------------------------------
def staff_required(view):
    return user_passes_test(lambda u: u.is_staff)(view)


@staff_required
def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price', 0)
        Product.objects.create(name=name, price=price)
        messages.success(request, 'Product created')
        return redirect('shop:shop_home')

    return render(request, 'shop/admin/product_form.html')


@staff_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.save()
        messages.success(request, 'Product updated')
        return redirect('shop:shop_home')

    return render(request, 'shop/admin/product_form.html', {'product': product})


@staff_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product deleted')
    return redirect('shop:shop_home')

@login_required
def order_history_api(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    data = []

    for order in orders:
        data.append({
            'order_id': order.id,
            'total_amount': float(order.total_amount()),
            'payment_method': order.payment_method,
            'status': order.status,
            'created_at': order.created_at
        })

    return JsonResponse({'orders': data})


# -------------------------------------------------
# Categories & Search
# -------------------------------------------------
def category_list(request):
    """Display all categories"""
    categories = Category.objects.all()
    return render(request, 'shop/category_list.html', {'categories': categories})


def category_products(request, slug):
    """Display products by category with subcategory filtering"""
    category = get_object_or_404(Category, slug=slug)
    subcategories = category.subcategories.all()
    
    # Get filter parameters
    subcategory_slug = request.GET.get('subcategory')
    search_query = request.GET.get('q', '')
    
    # Base query
    products = Product.objects.filter(category_ref=category)
    
    # Apply subcategory filter
    if subcategory_slug:
        subcategory = get_object_or_404(Subcategory, slug=subcategory_slug, category=category)
        products = products.filter(subcategory=subcategory)
    
    # Apply search within category
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'category': category,
        'subcategories': subcategories,
        'products': products,
        'search_query': search_query,
        'selected_subcategory': subcategory_slug
    }
    
    return render(request, 'shop/category_products.html', context)


def global_search(request):
    """Global search across all products"""
    query = request.GET.get('q', '')
    products = []
    count = 0
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(category_ref__name__icontains=query)
        ).distinct()
        count = products.count()
    
    return render(request, 'shop/search_results.html', {
        'query': query,
        'products': products,
        'count': count
    })


def random_products_api(request):
    """Return a random set of products for homepage auto-refresh with discount information."""
    count = int(request.GET.get('count', 24))
    items = []
    for p in Product.objects.order_by('?')[:count]:
        # Always return media URL for image
        if p.image:
            image_url = f"/media/{str(p.image)}"
        else:
            image_url = "/media/photos/default photo.jpg"
        
        # Get discount info
        discount_info = p.discount_info
        
        items.append({
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'discounted_price': float(discount_info['discounted_price']),
            'has_discount': discount_info['has_discount'],
            'discount_percentage': discount_info['percentage'],
            'savings': float(discount_info['savings']),
            'category': getattr(p.category_ref, 'name', None) or p.category or 'Uncategorized',
            'image': image_url
        })
    return JsonResponse({'products': items})


def _fuzzy_find(names, query, limit=5):
    """Return close matches for a misspelled query using simple ratio."""
    try:
        from difflib import get_close_matches
        return get_close_matches(query, names, n=limit, cutoff=0.6)
    except Exception:
        return []


def suggestions_api(request):
    """Return autocomplete suggestions for header/category search.
    - Blends partial (`icontains`) and fuzzy matches
    - Optional scoping by category slug via ?category=<slug>
    - Caps and deduplicates results
    """
    q = (request.GET.get('q') or '').strip()
    category_slug = request.GET.get('category')
    limit_total = int(request.GET.get('limit', 8))

    suggestions = []
    seen = set()  # track (type,label)
    def add_suggestion(it):
        key = (it['type'], it['label'])
        if key in seen:
            return False
        seen.add(key)
        suggestions.append(it)
        return True

    if not q:
        return JsonResponse({'suggestions': suggestions})

    # 1) Exact/partial contains
    # Categories
    for c in Category.objects.filter(name__icontains=q).order_by('name')[:5]:
        if len(suggestions) >= limit_total: break
        add_suggestion({
            'type': 'category', 'label': c.name, 'slug': c.slug,
            'url': reverse('shop:category_products', args=[c.slug])
        })

    # Subcategories (scoped to category if provided)
    sub_qs = Subcategory.objects.all()
    if category_slug:
        sub_qs = sub_qs.filter(category__slug=category_slug)
    for s in sub_qs.filter(name__icontains=q).order_by('name')[:5]:
        if len(suggestions) >= limit_total: break
        add_suggestion({
            'type': 'subcategory', 'label': s.name, 'slug': s.slug, 'category': s.category.slug,
            'url': reverse('shop:category_products', args=[s.category.slug]) + f'?subcategory={s.slug}'
        })

    # Products by name (contains)
    for p in Product.objects.filter(name__icontains=q).order_by('name')[:5]:
        if len(suggestions) >= limit_total: break
        add_suggestion({
            'type': 'product', 'label': p.name, 'id': p.id,
            'url': reverse('shop:product_detail', args=[p.id])
        })

    # 2) Fuzzy matches (added even when partial matches exist, until reaching limit)
    remaining = max(0, limit_total - len(suggestions))
    if remaining > 0:
        # Fuzzy Categories
        all_cat_names = list(Category.objects.values_list('name', flat=True))
        for name in _fuzzy_find(all_cat_names, q, limit=remaining):
            c = Category.objects.filter(name=name).first()
            if c and add_suggestion({
                'type': 'category', 'label': c.name, 'slug': c.slug,
                'url': reverse('shop:category_products', args=[c.slug])
            }):
                remaining = max(0, limit_total - len(suggestions))
                if remaining == 0:
                    break

    remaining = max(0, limit_total - len(suggestions))
    if remaining > 0:
        # Fuzzy Subcategories (respect category scope)
        sub_names_qs = Subcategory.objects.all()
        if category_slug:
            sub_names_qs = sub_names_qs.filter(category__slug=category_slug)
        all_sub_names = list(sub_names_qs.values_list('name', flat=True))
        for name in _fuzzy_find(all_sub_names, q, limit=remaining):
            s = Subcategory.objects.filter(name=name).first()
            if s and add_suggestion({
                'type': 'subcategory', 'label': s.name, 'slug': s.slug, 'category': s.category.slug,
                'url': reverse('shop:category_products', args=[s.category.slug]) + f'?subcategory={s.slug}'
            }):
                remaining = max(0, limit_total - len(suggestions))
                if remaining == 0:
                    break

    remaining = max(0, limit_total - len(suggestions))
    if remaining > 0:
        # Fuzzy Products: scope by category if provided; otherwise prefilter by first 3 chars to improve recall
        prod_qs = Product.objects.all()
        if category_slug:
            prod_qs = prod_qs.filter(category_ref__slug=category_slug)
        if len(q) >= 3 and not category_slug:
            prod_qs = prod_qs.filter(name__icontains=q[:3])
        # cap candidate pool size
        candidate_names = list(prod_qs.values_list('name', flat=True)[:1000])
        for name in _fuzzy_find(candidate_names, q, limit=remaining):
            p = Product.objects.filter(name=name).first()
            if p and add_suggestion({
                'type': 'product', 'label': p.name, 'id': p.id,
                'url': reverse('shop:product_detail', args=[p.id])
            }):
                remaining = max(0, limit_total - len(suggestions))
                if remaining == 0:
                    break

    return JsonResponse({'suggestions': suggestions, 'count': len(suggestions)})


# -------------------------------------------------
# Payments
# -------------------------------------------------
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse

import json
import datetime

@method_decorator(csrf_exempt, name='dispatch')
class PaymentWebhook(View):
    """Handle asynchronous payment notifications from the payment gateway."""
    def post(self, request, *args, **kwargs):
        # 1. Parse the JSON payload
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(status=400)

        # 2. Validate the payload (basic example, expand as needed)
        required_fields = ['order_id', 'status', 'amount', 'currency']
        if not all(field in payload for field in required_fields):
            return HttpResponse(status=400)

        # 3. Extract data
        order_id = payload['order_id']
        status = payload['status']
        amount = payload['amount']
        currency = payload['currency']

        # 4. Update the order in the database
        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.paid_amount = amount  # Update the paid amount
            order.payment_date = datetime.datetime.now()  # Set the payment date
            order.save()

            # If payment is successful, you might want to update stock, etc.
            if status == 'successful':
                for item in order.items.all():
                    # For each item in the order, reduce the stock quantity
                    if item.size:
                        # If the item has a size, find the corresponding ProductSize
                        product_size = ProductSize.objects.get(product=item.product, size=item.size)
                        product_size.quantity -= item.quantity
                        product_size.save()
                    else:
                        # For non-sized items, reduce the general product stock
                        item.product.stock -= item.quantity
                        item.product.save()

        except Order.DoesNotExist:
            return HttpResponse(status=404)
        except Exception as e:
            # Log the exception e
            return HttpResponse(status=500)

        # 5. Send a 200 OK response to acknowledge receipt of the webhook
        return HttpResponse(status=200)

@login_required
def confirm_payment(request, order_id):
    """Finalize: backfill missing item prices and recompute totals."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    with transaction.atomic():
        total = Decimal("0.00")
        for item in order.items.select_related('product').all():
            if item.price is None or item.price == 0:
                item.price = Decimal(str(getattr(item.product, "price", 0) or 0))
                item.save(update_fields=["price"])
            total += item.price * item.quantity

        fields = []
        if hasattr(order, "total_amount"):
            order.total_amount = total
            fields.append("total_amount")
        if hasattr(order, "total_price"):
            order.total_price = total
            fields.append("total_price")
        if hasattr(order, "final_total"):
            order.final_total = total + (order.delivery_fee or Decimal("0.00"))
            fields.append("final_total")
        order.save(update_fields=fields or None)

    return redirect('shop:orders_list')