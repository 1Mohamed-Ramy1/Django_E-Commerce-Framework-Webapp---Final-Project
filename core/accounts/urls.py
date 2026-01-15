from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile, name='home'),  # Also accessible as accounts:home
    path('profile/', views.profile, name='profile'),  # Preferred name
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('enter-activation-code/', views.EnterActivationCode, name='enter-activation-code'),
    path('reset-password/<str:activation_code>/', views.ResetPassword, name='reset-password'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
]
