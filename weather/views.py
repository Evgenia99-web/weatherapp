from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
import urllib.request
import requests
import json
import time
import datetime
from .models import City, CurrentWeather, CityStats, create_current_weather
from .serializers import CitySerializer, UserSerializer, CurrentWeatherSerializer, ProfileSerializer, HistorySerializer, FavoriteSerializer
from .permissions import IsOwnerOrReadOnly
from user.models import History, Favorite, Profile


# Create your views here.
def home(request):
    if request.method == 'POST':

        city = request.POST['city']

        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=0cd025f454e715b6b8c43a4329e68309&lang=ru'
        # convert  json file into python dectionary
        list_of_data = requests.get(url.format(city)).json()

        if str(list_of_data['cod']) == '404':
            return render(request, 'search_fail.html', {
                'error_message': f'Город "{city}" не найден! Возможно Вы ошиблись, попробуйте снова.'
            })
        elif str(list_of_data['cod']) != '200':
            return render(request, 'search_fail.html', {
                'error_message': ' Ощибка OpenWeather API! Возможно такого города нет в базе сервиса.'
            })

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
            'lon': float(list_of_data['coord']['lon']),

        }

        if not City.objects.filter(name=city):
            city_data = City(
                name=data['city'],
                country_code=data['country_code'],
                openweather_id=data['openweather_id'],
                latitude=data['lat'],
                longitude=data['lon']
            )
            city_data.save()

        if request.user.is_authenticated:
            history_data = History(
                city_name=City.objects.get(name=city),
                user_name=request.user,
                search_date=datetime.datetime.now()
            )
            history_data.save()

        current_city = City.objects.get(name=city)
        if Favorite.objects.filter(city_name=current_city):
            city_fav = True
        else:
            city_fav = False

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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by('user')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all().order_by('city_name')
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all().order_by('city_name')
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all().order_by('name')
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CurrentWeatherViewSet(viewsets.ModelViewSet):
    queryset = CurrentWeather.objects.all().order_by('city')
    serializer_class = CurrentWeatherSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
