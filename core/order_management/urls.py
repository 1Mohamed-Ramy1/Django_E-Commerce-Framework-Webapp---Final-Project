from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/invoice/', views.download_invoice, name='download_invoice'),
]
