from modeltranslation.translator import register, TranslationOptions
from .models import City, CurrentWeather
from user.models import Profile, History, Favorite


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(CurrentWeather)
class CurrentWeatherTranslationOptions(TranslationOptions):
    fields = ('desc_short',)


@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = ('country', 'city', )


@register(History)
class HistoryTranslationOptions(TranslationOptions):
    fields = ('city_name', )


@register(Favorite)
class FavoriteTranslationOptions(TranslationOptions):
    fields = ('city_name', )
