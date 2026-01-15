from django.utils import timezone
from weather.models import SearchHistory
from shop.models import Category

def global_header_data(request):
    recent_weather = SearchHistory.objects.order_by('-searched_at').first()
    recent_weather_list = SearchHistory.objects.filter(
        temperature__isnull=False
    ).order_by('-searched_at')[:5]
    categories = Category.objects.all().order_by('name')
    return {
        'recent_weather': recent_weather,
        'recent_weather_list': recent_weather_list,
        'now': timezone.now(),
        'all_categories': categories,
    }
