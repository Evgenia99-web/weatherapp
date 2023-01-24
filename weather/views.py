from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
import urllib.request
import requests
import json
import time
import datetime
from .models import City, CurrentWeather, CityStats, create_current_weather


# Create your views here.
def home(request):

    if request.method == 'POST':

        city = request.POST['city']

        source = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&appid=0cd025f454e715b6b8c43a4329e68309&lang=ru').read()

        # convert  json file into python dectionary
        list_of_data = json.loads(source)

        data = {
            'country_code': str(list_of_data['sys']['country']),
            'cor': str(list_of_data["coord"]["lon"]) + " " + str(list_of_data["coord"]["lat"]),
            'temp': int(list_of_data["main"]['temp']),
            'temp_min': int(list_of_data["main"]['temp_min']),
            'temp_max': int(list_of_data["main"]['temp_max']),
            'pressure': str(list_of_data['main']["pressure"]),
            'humidity': str(list_of_data['main']['humidity']),
            'wind': str(list_of_data['wind']['speed']),
            'sunrise': time.strftime("%H:%M", time.localtime((list_of_data['sys']['sunrise']))),
            'sunset': time.strftime("%H:%M", time.localtime((list_of_data['sys']['sunset']))),
            'main': str(list_of_data["weather"][0]['main']),
            'description': str(list_of_data["weather"][0]['description']),
            'icon': list_of_data["weather"][0]['icon'],
            'openweather_id': list_of_data['id'],
            'city': city,
            'lat': float(list_of_data['coord']['lat']),
            'lon': float(list_of_data['coord']['lon'])
        }

        city_data = City(
                name=data['city'],
                country_code=data['country_code'],
                openweather_id=data['openweather_id'],
                latitude=data['lat'],
                longitude=data['lon']
        )
        city_data.save()

    else:
        data = {}
    return render(request, 'weather_search.html', data)


def city_detail(request, city_name, city_openweather_id):
    city_set = City.objects.filter(openweather_id=city_openweather_id)

    if not city_set or city_set[0].name != city_name:
        raise Http404(f'City {city_name} with OpenWeather id {city_openweather_id} not found!')

    city = city_set[0]
    try:
        current_weather = city.weather
    except ObjectDoesNotExist:
        current_weather = create_current_weather(city, city_openweather_id)

    if not current_weather.was_updated_last_minute():
        current_weather.update()

    return render(request, 'city_detail.html', {'city': city, 'weather': current_weather})
