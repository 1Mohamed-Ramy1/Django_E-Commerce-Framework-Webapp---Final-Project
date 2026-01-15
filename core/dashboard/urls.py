from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard Home
    path('', views.dashboard_home, name='home'),

    # Products CRUD
    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.product_add, name="product_add"),
    path("products/edit/<int:pk>/", views.product_edit, name="product_edit"),
    path("products/delete/<int:pk>/", views.product_delete, name="product_delete"),

    # Users Management
    path("users/", views.users_list, name="users_list"),
    path("users/create/", views.create_user, name="create_user"),
    path("users/update/<int:pk>/", views.update_user, name="update_user"),
    path("users/delete/<int:pk>/", views.delete_user, name="delete_user"),
    path("users/warn/<int:pk>/", views.user_warn, name="user_warn"),

    # Events Management
    path("events/", views.event_list, name="event_list"),
    path("events/add/", views.event_add, name="event_add"),
    path("events/edit/<int:pk>/", views.event_edit, name="event_edit"),
    path("events/delete/<int:pk>/", views.event_delete, name="event_delete"),

    # Weather Management
    path('weather/', views.weather_list, name='weather_list'),
    path('weather/add/', views.weather_add, name='weather_add'),
    path('weather/edit/<int:pk>/', views.weather_edit, name='weather_edit'),
    path('weather/delete/<int:pk>/', views.weather_delete, name='weather_delete'),

    # Blog CRUD
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('blog/update/<int:pk>/', views.blog_update, name='blog_update'),
    path('blog/delete/<int:pk>/', views.blog_delete, name='blog_delete'),

    # Orders Management
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/status/', views.update_order_status, name='update_order_status'),
    path('orders/<int:pk>/cancel/', views.cancel_order, name='cancel_order'),
]
