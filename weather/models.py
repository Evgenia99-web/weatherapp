from django.db import models
from django.utils import timezone
import requests
import datetime
import urllib.request
from PIL import Image


class City(models.Model):
    name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=3)
    openweather_id = models.IntegerField(default=0, unique=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    image = models.ImageField(default='city_default.jpg', upload_to='city_pics')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 480 or img.width > 800:
            output_size = (800, 480)
            img.thumbnail(output_size)
            img.save(self.image.path)


class CurrentWeather(models.Model):
    # city = models.ForeignKey(City, on_delete=models.CASCADE)
    city = models.OneToOneField(City, on_delete=models.CASCADE, primary_key=True, related_name="weather")
    temp = models.FloatField(default=0)
    feels_like = models.FloatField(default=0)
    pressure = models.IntegerField(default=0)
    humidity = models.IntegerField(default=0)
    wind_speed = models.FloatField(default=0)
    desc_short = models.CharField('short description', max_length=30)
    icon_name = models.CharField(max_length=10)

    last_update = models.DateTimeField()

    def was_updated_last_minute(self):
        now = timezone.now()
        return now - datetime.timedelta(minutes=1) <= self.last_update <= now

    def update(self):
        url = 'http://api.openweathermap.org/data/2.5/weather?id={}&units=metric&appid=0cd025f454e715b6b8c43a4329e68309'
        response = requests.get(url)
        data = response.json()

        if str(data['cod']) != '200':
            print("OpenWeather update failed!")
            return

        self.temp = data['main']['temp']
        self.feels_like = data['main']['feels_like']
        self.pressure = data['main']['pressure']
        self.humidity = data['main']['humidity']
        self.wind_speed = data['wind']['speed']
        self.desc_short = data['weather'][0]['main']
        self.icon_name = data['weather'][0]['icon']
        self.last_update = timezone.now()
        self.save()

    class Meta:
        verbose_name = 'Прогноз'
        verbose_name_plural = 'Прогнозы'

    def __str__(self):
        return self.city.name


class CityStats(models.Model):
    city = models.OneToOneField(City,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name="stats")
    views = models.IntegerField(default=0)

    def inc_views(self):
        self.views += 1
        self.save()

    class Meta:
        verbose_name = 'Статистика по городу'
        verbose_name_plural = 'Статистика по городам'

    def __str__(self):
        return self.city.name


class StatsSummary(CityStats):
    class Meta:
        proxy = True
        verbose_name = "Дашборд"
        verbose_name_plural = "Дашборд"


def create_current_weather(city, openweather_id):
    # TODO handle failed requests
    url = 'http://api.openweathermap.org/data/2.5/weather?id='+ str(openweather_id)+'&units=metric&appid=0cd025f454e715b6b8c43a4329e68309'
    response = requests.get(url)
    weather_json = response.json()
    current_weather = CurrentWeather(
        city=city,
        temp=weather_json['main']['temp'],
        feels_like=weather_json['main']['feels_like'],
        pressure=weather_json['main']['pressure'],
        humidity=weather_json['main']['humidity'],
        wind_speed=weather_json['wind']['speed'],
        desc_short=weather_json['weather'][0]['main'],
        icon_name=weather_json['weather'][0]['icon'],
        last_update=timezone.now()
    )
    current_weather.save()
    return current_weather
