from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Shop
    path('', views.shop_home, name='shop_home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # Cart (DB-based)
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),  # wrapper
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Checkout & Orders
    path('checkout-page/', views.checkout_page, name='checkout_page'),
    path('orders/', views.orders_list, name='orders_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),

    # Admin CRUD
    path('admin/products/create/', views.create_product, name='create_product'),
    path('admin/products/<int:pk>/edit/', views.update_product, name='update_product'),
    path('admin/products/<int:pk>/delete/', views.delete_product, name='delete_product'),

    # API Orders
    path('api/orders/', views.order_history_api, name='order_history_api'),

    # Homepage random products API
    path('api/random-products/', views.random_products_api, name='random_products_api'),
    path('api/suggestions/', views.suggestions_api, name='suggestions_api'),

    # Categories & Search
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('search/', views.global_search, name='global_search'),

]
