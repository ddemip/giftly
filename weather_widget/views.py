import requests
from django.http import JsonResponse

API_KEY = 'eafc620f2fa0a2b539b67a1a05ab4aa9'
GEO_URL = "http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
BASE_URL_FORECAST = "http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"

def get_lat_lon(city):
    """
    Html asks for city input. Forecast needs latitude-longitude instead of city,
    this will get this information.
    """
    url = GEO_URL.format(city=city, api_key=API_KEY)
    response = requests.get(url)
    data = response.json()
    if not data:
        return None, None
    return data[0]['lat'], data[0]['lon']

def get_weather_data(city):
    """
    Uses get_lat_lon(city) function to get lat-lon for city,
    then asks info from openweathermap and returns city as json result.
    """
    lat, lon = get_lat_lon(city)
    if not lat or not lon:
        return None
    url = BASE_URL_FORECAST.format(lat=lat, lon=lon, api_key=API_KEY)
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

def fetch_weather(request):
    """
    Gets location value from html input, if gets city,
    then fetches weather data from openweathermap,
    builds a forecast and returns json response.
    """
    # Location input from html, JS makes AJAX POST request to this function,
    # this processes the request, fetches weather data from openweathermap,
    # returns weather data json response. Then JS processes that data,
    # creates html elements and updates weather widget by itself.

    city = request.POST.get('location')
    if city:
        weather_data = get_weather_data(city)
        if weather_data:
            forecasts = []
            for entry in weather_data['list']:
                forecasts.append({
                    'date_time': entry['dt_txt'],
                    'temperature': entry['main']['temp'],
                    'description': entry['weather'][0]['description'],
                    'icon': entry['weather'][0]['icon']
                })
            return JsonResponse({
                'city': city,
                'forecasts': forecasts
            })
    return JsonResponse({'error': 'City not found'}, status=404)
