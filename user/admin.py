from django.contrib import admin
from .models import Profile, History, Favorite
from modeltranslation.admin import TranslationAdmin


@admin.register(Profile)
class CityAdmin(TranslationAdmin):
    list_display = ("user", "city",)


@admin.register(History)
class CityAdmin(TranslationAdmin):
    list_display = ("user_name", "city_name", "search_date",)


@admin.register(Favorite)
class CityAdmin(TranslationAdmin):
    list_display = ("user_name", "city_name",)
