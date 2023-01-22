from django.shortcuts import render
import urllib.request
import json
import time


# Create your views here.
def home(request):
    if request.method == 'POST':

        city = request.POST['city']
        # retrieve imformation from weather api = https://api.openweathermap.org/api
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
            'sunrise': time.strftime("%H:%M", time.gmtime((list_of_data['sys']['sunrise']))),
            'sunset': time.strftime("%H:%M", time.gmtime((list_of_data['sys']['sunset']))),
            'main': str(list_of_data["weather"][0]['main']),
            'description': str(list_of_data["weather"][0]['description']),
            'icon': list_of_data["weather"][0]['icon'],
            'city': city
        }
    else:
        data = {}
    return render(request, 'weather_search.html', data)
