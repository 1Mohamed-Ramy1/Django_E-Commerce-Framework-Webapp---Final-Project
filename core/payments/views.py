from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404, render, redirect
from order_management.models import Order
from .models import Payment
from reportlab.pdfgen import canvas
import os

@login_required
def countdown(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    session_key = f'payment_countdown_done_{order.id}'

    # If payment already completed or countdown was finished, don't show countdown again
    if getattr(order, 'payment', None) and order.payment.is_paid:
        return redirect('shop:view_cart')
    if request.session.get(session_key):
        return redirect('shop:view_cart')

    return render(request, 'payments/countdown.html', {'order': order})


@login_required
def confirm_payment(request, order_id):
    from accounts.models import Profile
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # get payment safely
    payment = getattr(order, 'payment', None)

    # Confirm the payment (if present)
    if payment and not payment.is_paid:
        payment.confirm()

    # mark countdown as completed in session so it won't reappear
    request.session[f'payment_countdown_done_{order.id}'] = True

    # Get or create profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    # Calculate and add points
    try:
        points_earned = int(order.final_total // 10)
    except Exception:
        points_earned = 0
    profile.points += points_earned
    profile.save()

    # Prepare context for thank you page
    context = {
        'order': order,
        'points_earned': points_earned,
        'total_points': profile.points,
    }

    return render(request, 'payments/thank_you.html', context)


@login_required
def cancel_order(request, order_id):
    """Allow user to cancel a pending order so they can checkout again."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != 'pending':
        messages.info(request, 'Order is not pending and cannot be cancelled.')
        return redirect('shop:view_cart')

    order.status = 'cancelled'
    order.save()
    # remove related payment record if it exists
    try:
        if hasattr(order, 'payment') and order.payment:
            order.payment.delete()
    except Exception:
        pass

    messages.success(request, 'Pending order cancelled. You can now place a new order.')
    return redirect('shop:view_cart')

    

@login_required
def invoice_pdf(request, order_id):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from datetime import datetime, timedelta, timezone
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Get current time in Cairo timezone (UTC+2)
    current_utc = datetime.now(timezone.utc)
    order_date = current_utc + timedelta(hours=2)
    
    file_name = f"receipt_{order.id}.pdf"
    file_path = os.path.join('media', 'invoices', file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Create PDF
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1a73e8'),
        spaceAfter=6,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#333333')
    )
    
    # Store Name - Big and Bold
    store_name = Paragraph("<b>🏪 ELOSTORA STORE</b>", title_style)
    elements.append(store_name)
    elements.append(Spacer(1, 0.3*inch))
    
    # Receipt Header
    invoice_data = [
        ['Receipt #', str(order.id)],
        ['Date & Time', order_date.strftime('%d %b %Y - %I:%M %p')],
        ['Customer', request.user.username],
        ['Payment Method', order.payment.method.upper()],
        ['Status', '✓ COMPLETED'],
    ]
    
    invoice_table = Table(invoice_data, colWidths=[2*inch, 4*inch])
    invoice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    elements.append(invoice_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Items Header
    elements.append(Paragraph("<b>Order Items</b>", heading_style))
    
    # Items Table
    items_data = [['Product', 'Qty', 'Size', 'Price', 'Total']]
    
    for item in order.items.all():
        items_data.append([
            item.product.name,
            str(item.quantity),
            item.size if hasattr(item, 'size') else '—',
            f'${item.product.price}',
            f'${float(item.product.price * item.quantity):.2f}'
        ])
    
    items_table = Table(items_data, colWidths=[2.5*inch, 0.8*inch, 0.8*inch, 1*inch, 1*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9f9f9')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Summary
    summary_data = [
        ['Subtotal:', f'${order.total_amount}'],
        ['Delivery Fee (5%):', f'${order.delivery_fee}'],
        ['', ''],
        ['TOTAL:', f'${order.final_total}'],
    ]
    
    summary_table = Table(summary_data, colWidths=[4*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 2), 'Helvetica'),
        ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 3), (-1, 3), 14),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#1a73e8')),
        ('TEXTCOLOR', (0, 3), (-1, 3), colors.white),
        ('TOPPADDING', (0, 3), (-1, 3), 8),
        ('BOTTOMPADDING', (0, 3), (-1, 3), 8),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer_text = "<i>Thank you for shopping with ELOSTORA STORE! We appreciate your business.</i>"
    elements.append(Paragraph(footer_text, normal_style))
    
    # Build PDF
    doc.build(elements)

    return FileResponse(open(file_path, 'rb'), content_type='application/pdf', as_attachment=True, filename=file_name)

