from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Public Blog
    path('', views.public_blog_list, name='public_list'),
    path('post/<int:id>/', views.public_blog_detail_by_id, name='public_detail_id'),  # NEW - for product news
    path('post/<slug:slug>/', views.public_blog_detail, name='public_detail'),  # For actual blog posts
    
    # Dashboard CRUD
    path('dashboard/', views.blog_list, name='blog_list'),
    path('dashboard/create/', views.blog_create, name='blog_create'),
    path('dashboard/update/<int:pk>/', views.blog_update, name='blog_update'),
    path('dashboard/delete/<int:pk>/', views.blog_delete, name='blog_delete'),
]