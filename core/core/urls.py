from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import home_redirect

urlpatterns = [
    path('', home_redirect, name='root'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('shop/', include('shop.urls')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('events/', include('events.urls')),
    path('weather/', include('weather.urls')),
    path('payments/', include('payments.urls')),
    path('orders/', include('order_management.urls')),
    path('gifts/', include('gift.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
