from django.urls import path
from . import views

app_name = 'gift'

urlpatterns = [
    path('', views.gift_list, name='gift_list'),
    path('redeem/<uuid:uid>/', views.redeem_gift, name='redeem_gift'),
    path('my-redemptions/', views.my_redemptions, name='my_redemptions'),
]
