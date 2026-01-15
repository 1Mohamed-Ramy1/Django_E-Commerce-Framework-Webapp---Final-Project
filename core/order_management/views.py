from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from payments.views import invoice_pdf

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': order.items.all(),
        'payment': getattr(order, 'payment', None)
    })

@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status='completed')
    return invoice_pdf(request, order.id)