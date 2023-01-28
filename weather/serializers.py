from rest_framework import serializers
from django.contrib.auth.models import User
from .models import City, CurrentWeather
from user.models import Profile, History, Favorite


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'country_code', 'openweather_id', 'latitude', 'longitude', 'image')


class CurrentWeatherSerializer(serializers.HyperlinkedModelSerializer):
    city = serializers.HyperlinkedRelatedField(view_name='city-detail', queryset=City.objects.all())

    class Meta:
        model = CurrentWeather
        fields = ('city', 'temp', 'feels_like', 'pressure', 'humidity', 'wind_speed', 'desc_short', 'icon_name')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', queryset=User.objects.all())

    class Meta:
        model = Profile
        fields = ('user', 'country', 'city', 'image')


class HistorySerializer(serializers.HyperlinkedModelSerializer):
    user_name = serializers.HyperlinkedRelatedField(view_name='user-detail', queryset=User.objects.all())
    city_name = serializers.HyperlinkedRelatedField(view_name='city-detail', queryset=City.objects.all())

    class Meta:
        model = History
        fields = ('city_name', 'user_name', 'search_date')


class FavoriteSerializer(serializers.HyperlinkedModelSerializer):
    user_name = serializers.HyperlinkedRelatedField(view_name='user-detail', queryset=User.objects.all())
    city_name = serializers.HyperlinkedRelatedField(view_name='city-detail', queryset=City.objects.all())

    class Meta:
        model = Favorite
        fields = ('city_name', 'user_name')