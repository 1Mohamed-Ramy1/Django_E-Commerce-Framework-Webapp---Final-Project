from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('countdown/<int:order_id>/', views.countdown, name='countdown'),
    path('confirm/<int:order_id>/', views.confirm_payment, name='confirm_payment'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('invoice/<int:order_id>/', views.invoice_pdf, name='invoice_pdf'),
]
