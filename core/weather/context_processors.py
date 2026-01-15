from datetime import datetime
from .models import SearchHistory

def global_weather(request):
    recent_weather = SearchHistory.objects.order_by('-id').first()
    now = datetime.now()
    return {
        'recent_weather': recent_weather,
        'now': now,
    }
