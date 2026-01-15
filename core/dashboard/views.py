# core/dashboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from order_management.models import Order, OrderItem
from django.views.decorators.cache import never_cache

from shop.models import Product, ProductSize
from events.models import Event
from weather.models import SearchHistory
from blog.models import Post

from .forms import ProductForm, EventForm, WeatherForm, UserForm, PostForm

# --------------------------------
# decorator: only staff/admin
# --------------------------------
def staff_required(view):
    return user_passes_test(lambda u: u.is_staff)(view)

# --------------------------------
# Dashboard home (summary)
# --------------------------------
@staff_required
@never_cache
def dashboard_home(request):
    products_count = Product.objects.count()
    users_count = User.objects.count()
    events_count = Event.objects.count()
    posts_count = Post.objects.count()
    weather_count = SearchHistory.objects.count()

    context = {
        'products_count': products_count,
        'users_count': users_count,
        'events_count': events_count,
        'blog_count': posts_count,
        'weather_count': weather_count,
    }
    return render(request, 'dashboard/home.html', context)


# -------------------------------
# Products CRUD (admin)
# -------------------------------
@staff_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'dashboard/product_list.html', {'products': products})

@staff_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect('dashboard:product_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProductForm()
    return render(request, 'dashboard/product_form.html', {'form': form, 'action': 'Add'})

@staff_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('dashboard:product_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/product_form.html', {'form': form, 'action': 'Edit', 'product': product})

@staff_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect('dashboard:product_list')
    return render(request, "dashboard/product_confirm_delete.html", {"product": product})


# -------------------------------
# Users CRUD (admin)
# -------------------------------
@staff_required
def users_list(request):
    users = User.objects.all()
    
    # Order by ID to ensure ELOSTORA (ID=1) is at the top
    users = users.order_by('id')
    
    # Don't exclude ELOSTORA anymore - show it but with different permissions
    if not request.user.is_superuser:
        # Manager can see ELOSTORA but not edit/delete it
        users = users.exclude(is_superuser=True).exclude(username='admin')
    
    return render(request, 'dashboard/users_list.html', {'users': users})

@staff_required
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Ensure password provided when creating a new user
            pwd = form.cleaned_data.get('password')
            if not pwd:
                messages.error(request, "Password is required when creating a new user.")
            else:
                form.save()
                messages.success(request, "User created successfully.")
                return redirect('dashboard:users_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserForm()
    return render(request, 'dashboard/user_form.html', {'form': form, 'action': 'Create'})

@staff_required
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # Allow ELOSTORA to edit their own account
    # Prevent other managers from editing ELOSTORA or admin accounts
    if user.username.lower() == 'elostora':
        # Only ELOSTORA can edit ELOSTORA account
        if request.user.username.lower() != 'elostora':
            messages.error(request, "You don't have permission to edit this user.")
            return redirect('dashboard:users_list')
    elif not request.user.is_superuser and (user.is_superuser or user.username.lower() == 'admin'):
        # Prevent non-superusers from editing other admin/superuser accounts
        messages.error(request, "You don't have permission to edit this user.")
        return redirect('dashboard:users_list')
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect('dashboard:users_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserForm(instance=user)
    return render(request, 'dashboard/user_form.html', {'form': form, 'action': 'Edit', 'user': user})

@staff_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # Prevent non-superusers from deleting admin/superuser accounts
    if not request.user.is_superuser and (user.is_superuser or user.username.lower() in ['admin', 'elostora']):
        messages.error(request, "You don't have permission to delete this user.")
        return redirect('dashboard:users_list')
    
    if request.method == "POST":
        user.delete()
        messages.success(request, "User deleted.")
        return redirect('dashboard:users_list')
    return render(request, "dashboard/user_confirm_delete.html", {"user": user})


# -------------------------------
# Events CRUD (admin)
# -------------------------------
@staff_required
def event_list(request):
    events = Event.objects.all()
    return render(request, 'dashboard/event_list.html', {'events': events})

@staff_required
def event_add(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event added successfully.")
            return redirect('dashboard:event_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = EventForm()
    return render(request, 'dashboard/event_form.html', {'form': form, 'action': 'Add'})

@staff_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('dashboard:event_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = EventForm(instance=event)
    return render(request, 'dashboard/event_form.html', {'form': form, 'action': 'Edit', 'event': event})

@staff_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted.")
        return redirect('dashboard:event_list')
    return render(request, "dashboard/event_confirm_delete.html", {"event": event})


# -------------------------------
# Weather CRUD (admin)
# -------------------------------
@staff_required
def weather_list(request):
    weather_entries = SearchHistory.objects.all()

    return render(request, 'dashboard/weather_list.html', {'weather_entries': weather_entries})

@staff_required
def weather_add(request):
    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Weather entry added successfully.")
            return redirect('dashboard:weather_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = WeatherForm()
    return render(request, 'dashboard/weather_form.html', {'form': form, 'action': 'Add'})

@staff_required
def weather_edit(request, pk):
    entry = get_object_or_404(SearchHistory, pk=pk)

    if request.method == 'POST':
        form = WeatherForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Weather entry updated successfully.")
            return redirect('dashboard:weather_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = WeatherForm(instance=entry)
    return render(request, 'dashboard/weather_form.html', {'form': form, 'action': 'Edit', 'entry': entry})

@staff_required
def weather_delete(request, pk):
    try:
        entry = SearchHistory.objects.get(pk=pk)
    except SearchHistory.DoesNotExist:
        messages.info(request, "Weather entry not found or already deleted.")
        return redirect('dashboard:weather_list')

    if request.method == 'POST':
        # Re-check existence in case it was removed between requests
        try:
            entry.delete()
            messages.success(request, "Weather entry deleted successfully.")
        except Exception:
            messages.error(request, "Could not delete weather entry. It may have been removed already.")
        return redirect('dashboard:weather_list')

    return render(request, 'dashboard/weather_confirm_delete.html', {'entry': entry})


# -------------------------------
# Blog CRUD (admin)
# -------------------------------
@staff_required
def blog_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'dashboard/blog_list.html', {'posts': posts})

@staff_required
def blog_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post created successfully.")
            return redirect('dashboard:blog_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = PostForm()
    return render(request, 'dashboard/blog_form.html', {'form': form, 'action': 'Add'})

@staff_required
def blog_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post updated successfully.")
            return redirect('dashboard:blog_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = PostForm(instance=post)
    return render(request, 'dashboard/blog_form.html', {'form': form, 'action': 'Edit', 'post': post})

@staff_required
def blog_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Blog post deleted successfully.")
        return redirect('dashboard:blog_list')
    return render(request, 'dashboard/blog_confirm_delete.html', {'post': post})

@staff_required
def user_warn(request, pk):
    user = get_object_or_404(User, pk=pk)

    profile = getattr(user, 'profile', None)
    if profile is None:
        messages.error(request, "User has no profile to warn.")
        return redirect('dashboard:users_list')
    profile.warning = True
    profile.save()
    messages.success(request, f"User {user.username} warned.")
    return redirect('dashboard:users_list')


@staff_required
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'dashboard/order_list.html', {'orders': orders})

@staff_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    items = order.items.all()
    return render(request, 'dashboard/order_detail.html', {
        'order': order,
        'items': items
    })

@staff_required
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        status = request.POST.get('status')
        current = order.status
        if status not in settings.ALLOWED_STATUS_FLOW.get(current, []):
            messages.error(request, "Invalid status transition.")
        else:
            order.status = status
            order.save()
            messages.success(request, "Order updated.")

    return redirect('dashboard:order_detail', pk=pk)

@staff_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

    
    if order.status != Order.STATUS_COMPLETED:
        for item in order.items.all():
            size = ProductSize.objects.get(
                product=item.product,
                size=item.size
            )
            size.quantity += item.quantity
            size.save()
    
    order.status = Order.STATUS_CANCELLED
    order.save()
    messages.success(request, "Order cancelled.")
    return redirect('dashboard:order_list')
    

from accounts.models import BalanceTransaction

@login_required
def wallet_history(request):
    transactions = BalanceTransaction.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'dashboard/wallet.html', {
        'transactions': transactions
    })

# -------------------------------
# Orders Management (admin)
# -------------------------------
@staff_required
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'dashboard/order_list.html', {'orders': orders})

@staff_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'dashboard/order_detail.html', {'order': order})

@staff_required
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
            messages.success(request, f"Order status updated to {status}.")
        else:
            messages.error(request, "Invalid status.")

    return redirect('dashboard:order_detail', pk=pk)
