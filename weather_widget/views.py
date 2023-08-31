import requests
from django.http import JsonResponse

API_KEY = 'eafc620f2fa0a2b539b67a1a05ab4aa9'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"

def get_weather_data(city):
    """Asks info from openweathermap and returns json result"""
    url = BASE_URL.format(city=city, api_key=API_KEY)
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

def fetch_weather(request):
    """api function which is ran by ajax request.
    In .html javascript ajax request based on url: "/weather_widget/fetch_weather/" to get weather info
    by location. Then returns json response described above."""
    city = request.POST.get('location')
    if city:
        weather_data = get_weather_data(city)
        if weather_data:
            return JsonResponse({
                'city': city,
                'temperature': weather_data['main']['temp'],
                'description': weather_data['weather'][0]['description']
            })
    return JsonResponse({'error': 'City not found'}, status=404)
