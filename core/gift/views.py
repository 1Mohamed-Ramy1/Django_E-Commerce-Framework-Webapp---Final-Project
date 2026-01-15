from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Gift, GiftRedemption
from django.core.mail import send_mail
from django.conf import settings

def gift_list(request):
    """Display all available gifts"""
    gifts = Gift.objects.filter(is_active=True)
    user_points = 0
    user_redemptions = []
    
    if request.user.is_authenticated:
        user_points = request.user.profile.points
        user_redemptions = GiftRedemption.objects.filter(user=request.user).select_related('gift')[:5]
    
    context = {
        'gifts': gifts,
        'user_points': user_points,
        'user_redemptions': user_redemptions,
    }
    return render(request, 'gift/gift_list.html', context)


@login_required
def redeem_gift(request, uid):
    """Process gift redemption"""
    gift = get_object_or_404(Gift, uid=uid, is_active=True)
    
    if request.method == 'POST':
        user = request.user
        profile = user.profile
        
        # Check if user has enough points
        if profile.points < gift.points_cost:
            messages.error(request, f'Not enough points! You need {gift.points_cost:,} points but have {profile.points:,}.')
            return redirect('gift:gift_list')
        
        # Check stock
        if gift.stock_quantity < 1:
            messages.error(request, 'Sorry, this gift is out of stock.')
            return redirect('gift:gift_list')
        
        # Process redemption
        try:
            with transaction.atomic():
                # Deduct points
                profile.points -= gift.points_cost
                profile.save()
                
                # Reduce stock
                gift.stock_quantity -= 1
                gift.save()
                
                # Create redemption record
                redemption = GiftRedemption.objects.create(
                    user=user,
                    gift=gift,
                    points_spent=gift.points_cost,
                    status='completed'
                    
                )
                send_mail(
                    subject='🎉 Gift Redeemed Successfully!',
                    message=(
                        f"Hi {user.username},\n\n"
                        f"Congratulations! 🎁 You have redeemed: {gift.name}.\n"
                        f"Points spent: {gift.points_cost}. Remaining points: {profile.points}.\n\n"
                        "Your gift has been added to your profile (My Gifts)."
                    ),
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                    recipient_list=[user.email] if user.email else [],
                    fail_silently=True,
                )
                
                messages.success(request, f"🎉 Congrats! {gift.name} has been added to your profile (My Gifts).")
                return redirect('gift:gift_list')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('gift:gift_list')
    
    context = {
        'gift': gift,
        'user_points': request.user.profile.points,
    }
    return render(request, 'gift/redeem_confirm.html', context)


@login_required
def my_redemptions(request):
    """View user's gift redemption history"""
    redemptions = GiftRedemption.objects.filter(user=request.user).select_related('gift')
    
    context = {
        'redemptions': redemptions,
        'user_points': request.user.profile.points,
    }
    return render(request, 'gift/my_redemptions.html', context)
