from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone

import random

from shop.models import Product
from .models import Post, Category
from .forms import PostForm


# -------------------------------------------------
# Public Blog = Product News
# -------------------------------------------------
def _news_copy_for_product(product: Product):
    """Deterministic 'news-style' copy per product (no DB writes)."""
    category_name = getattr(product.category_ref, 'name', None) or getattr(product, 'category', None) or 'Products'
    price = getattr(product, 'price', None)
    seed = (product.id or 0) * 97
    rng = random.Random(seed)

    title_templates = [
        "Market Watch: {name} is trending in {cat}",
        "New Arrival Spotlight: {name}",
        "Editor's Pick: {name} just landed", 
        "Today's Deal Radar: {name}",
        "What buyers love right now: {name}",
    ]
    subtitle_templates = [
        "A quick look at why it's getting attention — features, value, and where it fits.",
        "We broke down the highlights so you can decide fast.",
        "Here's what stands out, and what to check before you buy.",
        "Short, practical notes — no fluff.",
    ]

    title = rng.choice(title_templates).format(name=product.name, cat=category_name)
    subtitle = rng.choice(subtitle_templates)

    raw_desc = (getattr(product, 'description', '') or '').strip()
    if raw_desc:
        excerpt = raw_desc
    else:
        excerpt = f"{product.name} is one of our most notable picks in {category_name}."

    highlights = [f"Category: {category_name}"]
    if price is not None:
        highlights.append(f"Price: {price}")

    # Extra "news" metadata
    tags_pool = [
        'Trending', 'Editor Pick', 'Deal Watch', 'Just In', 'Buyer Favorite',
        'Best Value', 'Staff Choice', 'Top Rated',
    ]
    tags = rng.sample(tags_pool, k=2)

    # Reading time: 2–4 mins deterministic
    reading_time = 2 + (product.id % 3 if product.id else 2)

    # Deterministic "published" date within last ~14 days
    days_ago = (product.id % 14) if product.id else 7
    published_at = timezone.localdate() - timezone.timedelta(days=days_ago)

    why_matters_pool = [
        "Because it delivers practical value without overpaying.",
        "Because it hits the sweet spot between quality and everyday use.",
        "Because it's a strong pick if you want something reliable and straightforward.",
        "Because it's the kind of product that quietly becomes your daily go-to.",
    ]
    why_matters = rng.choice(why_matters_pool)

    # Simple "specs snapshot" built from available fields
    specs = []
    if getattr(product, 'subcategory', None):
        specs.append(("Subcategory", getattr(product.subcategory, 'name', '')))
    specs.append(("Category", category_name))
    if price is not None:
        specs.append(("Price", str(price)))

    pros_pool = [
        "Easy to compare and choose",
        "Solid pick for daily use",
        "Great balance of price and value",
        "Clean, simple, and practical",
        "Fits well in most setups",
    ]
    pros = rng.sample(pros_pool, k=3)

    best_for_pool = [
        "Everyday buyers",
        "Gift shopping",
        "Budget-conscious picks",
        "Upgrading your basics",
        "Anyone who wants a dependable option",
    ]
    best_for = rng.choice(best_for_pool)

    body_paras = [
        f"In today's {category_name.lower()} roundup, {product.name} is drawing attention for its balance of practicality and style.",
        "If you're comparing options, focus on fit, materials, and how it matches your day-to-day use — that's where value shows up.",
    ]
    if raw_desc:
        body_paras.append(raw_desc)

    closing = "Want the full specs and photos? Open the product page for the complete details."

    return {
        'tags': tags,
        'published_at': published_at,
        'reading_time': reading_time,
        'why_matters': why_matters,
        'specs': specs,
        'pros': pros,
        'best_for': best_for,
        'title': title,
        'subtitle': subtitle,
        'excerpt': ' '.join(excerpt.split()[:28]) + ('…' if len(excerpt.split()) > 28 else ''),
        'highlights': highlights,
        'body_paras': body_paras,
        'closing': closing,
    }


def public_blog_list(request):
    """Public blog feed: one 'post' per product, in a daily-shuffled order."""
    per_page = int(request.GET.get('per', 12))
    page_number = request.GET.get('page', 1)

    product_qs = Product.objects.all().select_related('category_ref', 'subcategory')

    product_ids = list(product_qs.values_list('id', flat=True))
    # Stable shuffle per day (so user can paginate and cover all products)
    seed = timezone.localdate().isoformat()
    rng = random.Random(seed)
    rng.shuffle(product_ids)

    paginator = Paginator(product_ids, per_page)
    page_obj = paginator.get_page(page_number)
    page_ids = list(page_obj.object_list)

    products = list(Product.objects.filter(id__in=page_ids).select_related('category_ref', 'subcategory'))
    by_id = {p.id: p for p in products}
    ordered_products = [by_id[i] for i in page_ids if i in by_id]

    items = []
    for p in ordered_products:
        items.append({
            'product': p,
            'news': _news_copy_for_product(p),
        })

    return render(request, 'blog/public_blog_list.html', {
        'items': items,
        'page_obj': page_obj,
        'seed': seed,
        'total_products': len(product_ids),
    })


def public_blog_detail(request, slug: str):
    """Public blog detail: actual blog post by slug."""
    post = get_object_or_404(Post, slug=slug, is_published=True)
    
    # Generate news-style context for template
    news_data = {
        'title': post.title,
        'subtitle': '',
        'tags': ['Blog', 'Article'],
        'reading_time': max(2, len(post.content.split()) // 200),
        'published_at': post.created_at.date(),
        'why_matters': '',
        'body_paras': [post.content],
        'closing': '',
        'highlights': [],
        'specs': [],
        'pros': [],
        'best_for': '',
        'excerpt': post.short_description(),
    }
    
    # Mock product for template compatibility
    class MockProduct:
        id = None
        name = post.title
        category = 'Blog'
        category_ref = None
        price = None
        description = ''
        image = post.image
    
    return render(request, 'blog/public_blog_detail.html', {
        'post': post,
        'news': news_data,
        'product': MockProduct(),
    })


def public_blog_detail_by_id(request, id: int):
    """Public blog detail: product 'news' by ID."""
    product = get_object_or_404(Product, id=id)
    
    news_data = _news_copy_for_product(product)
    
    class MockPost:
        title = product.name
        category = product.category_ref or product.category
        image = product.image
    
    return render(request, 'blog/public_blog_detail.html', {
        'post': MockPost(),
        'news': news_data,
        'product': product,
        'is_product_news': True,
    })


# Dashboard Blog Views
@staff_member_required
def blog_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'dashboard/blog_list.html', {'posts': posts})


@staff_member_required
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
    return render(
        request,
        'dashboard/blog_form.html',
        {
            'form': form,
            'action': 'Create',
        }
    )


@staff_member_required
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
    return render(
        request,
        'dashboard/blog_form.html',
        {
            'form': form,
            'action': 'Edit',
            'post': post,
        }
    )


@staff_member_required
def blog_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Blog post deleted successfully.")
        return redirect('dashboard:blog_list')
    return render(
        request,
        'dashboard/blog_confirm_delete.html',
        {'post': post}
    )