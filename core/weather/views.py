import requests
from .models import SearchHistory
from django.shortcuts import render, redirect
from django.conf import settings
API_KEY = '7e952d38356d445749098094c23aa2d8'

def index(request):
    weather = None
    if request.method == 'POST':
        city = request.POST.get('city')
        try:
            r = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
            )
            data = r.json()
            if r.status_code == 200:
                weather = {
                    'temp': data['main']['temp'],
                    'city': city
                }
                SearchHistory.objects.create(city_name=city, temperature=data['main']['temp'])
            else:
                weather = {'error': data.get('message', 'Error fetching weather')}
        except Exception as e:
            weather = {'error': str(e)}

    return render(request, 'weather/widget.html', {'weather': weather})

def weather_search(request):
    weather_data = None
    
    if request.method == "POST":
        city = request.POST.get("city")
        

        # Fetch weather from API with guard
        api_key = getattr(settings, 'WEATHER_API_KEY', None)
        if not api_key:
            weather_data = {'error': 'Weather API key is not configured.'}
            response = {}
        else:
            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                resp = requests.get(url, timeout=10)
                response = resp.json()
            except requests.RequestException:
                weather_data = {'error': 'Weather service is unreachable.'}
                response = {}

        # Parse
        if response.get("main"):
            weather_info = {
                'city': city.capitalize(),
                'temp': response["main"].get("temp"),
                'feels_like': response["main"].get("feels_like"),
                'humidity': response["main"].get("humidity"),
                'wind_speed': (response.get('wind') or {}).get('speed'),
                'condition': response["weather"][0].get("description").capitalize(),
                'icon': response["weather"][0].get("icon"),
            }
            weather_data = weather_info
            # Save full snapshot to history with graceful fallbacks
            SearchHistory.objects.create(
                city_name=weather_info['city'],
                temperature=weather_info.get('temp'),
                feels_like=weather_info.get('feels_like'),
                humidity=weather_info.get('humidity'),
                wind_speed=weather_info.get('wind_speed'),
                description=weather_info.get('condition'),
                icon=weather_info.get('icon'),
            )

    return render(request, "weather/search.html", {"weather":weather_data})