from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import PasswordReset 
from order_management.models import Order


def RegisterView(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        errors = False
        if User.objects.filter(username=username).exists():
            errors = True
            messages.error(request, "Username already exists")
        if User.objects.filter(email=email).exists():
            errors = True
            messages.error(request, "Email already exists")
        # Require Gmail addresses only
        if not (isinstance(email, str) and email.strip().lower().endswith('@gmail.com')):
            errors = True
            messages.error(request, "Email must be a Gmail address ending with @gmail.com")
        if len(password) < 5:
            errors = True
            messages.error(request, "Password must be at least 5 characters")

        if errors:
            return redirect('accounts:register')
        User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )
        messages.success(request, "Account created. Login now")
        return redirect('accounts:login')

    return render(request, 'accounts/register.html')


def LoginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # admin -> admin dashboard, normal user -> shop home
            if user.is_staff:
                return redirect('dashboard:home')
            return redirect('shop:shop_home')
        messages.error(request, "Invalid login credentials")
        return redirect('accounts:login')

    return render(request, 'accounts/login.html')

def LogoutView(request):
    messages.get_messages(request).used = True
    logout(request)
    return redirect('accounts:login')


def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Delete old reset requests for this user
            PasswordReset.objects.filter(user=user).delete()
            # Create new reset request with activation code
            reset = PasswordReset(user=user)
            reset.save()
            EmailMessage(
                'Password Reset - Activation Code',
                f'Your password reset activation code is:\n\n{reset.activation_code}\n\nThis code will expire in 5 minutes.\nEnter this code on the password reset page to continue.',
                settings.EMAIL_HOST_USER,
                [email]
            ).send(fail_silently=False)
            messages.success(request, f'Activation code sent to {email}. Please check your inbox.')
            return redirect('accounts:enter-activation-code')
        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('accounts:forgot-password')
    return render(request, 'accounts/forgot_password.html')


def EnterActivationCode(request):
    """View for entering the 6-digit activation code."""
    if request.method == "POST":
        code = request.POST.get('activation_code', '').strip()
        try:
            reset = PasswordReset.objects.get(activation_code=code)
            # Check if code expired (5 minutes)
            if timezone.now() > reset.created_when + timezone.timedelta(minutes=5):
                reset.delete()
                messages.error(request, 'Activation code has expired. Please request a new one.')
                return redirect('accounts:forgot-password')
            # Code is valid, redirect to change password
            return redirect('accounts:reset-password', activation_code=code)
        except PasswordReset.DoesNotExist:
            messages.error(request, 'Invalid activation code. Please try again.')
            return redirect('accounts:enter-activation-code')
    return render(request, 'accounts/enter_activation_code.html')


def ResetPassword(request, activation_code):
    try:
        reset = PasswordReset.objects.get(activation_code=activation_code)
        # Check if code expired
        if timezone.now() > reset.created_when + timezone.timedelta(minutes=5):
            reset.delete()
            messages.error(request, 'Activation code has expired')
            return redirect('accounts:forgot-password')
    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid activation code')
        return redirect('accounts:forgot-password')

    if request.method == "POST":
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')
        errors = False
        if password != confirm:
            errors = True
            messages.error(request, 'Passwords do not match')
        if len(password) < 5:
            errors = True
            messages.error(request, 'Password must be at least 5 characters')
        if errors:
            return redirect('accounts:reset-password', activation_code=activation_code)
        user = reset.user
        user.set_password(password)
        user.save()
        reset.delete()
        messages.success(request, 'Password reset. Proceed to login')
        return redirect('accounts:login')

    return render(request, 'accounts/reset_password.html')


def home_redirect(request):
    
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard:home')
        return redirect('shop:shop_home')
    return redirect('accounts:login')

@login_required
def profile(request):
    profile = request.user.profile
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    from gift.models import GiftRedemption
    gifts = GiftRedemption.objects.filter(user=request.user).select_related('gift').order_by('-redeemed_at')[:10]

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'orders': orders,
        'gifts': gifts
    })


@login_required
def edit_profile(request):
    from .forms import UserForm, ProfileForm
    
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            # detect if password was changed so session auth hash can be updated
            pwd = user_form.cleaned_data.get('password')
            user_form.save()
            profile_form.save()
            if pwd:
                # keep the user logged in after password change
                update_session_auth_hash(request, request.user)
            messages.success(request, 'Profile updated successfully')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please check the form for errors')

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
