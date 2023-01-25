from django.contrib import admin
from .models import Profile, History, Favorite


@admin.register(Profile)
class CityAdmin(admin.ModelAdmin):
    list_display = ("user", "city",)


@admin.register(History)
class CityAdmin(admin.ModelAdmin):
    list_display = ("user_name", "city_name", "search_date",)


@admin.register(Favorite)
class CityAdmin(admin.ModelAdmin):
    list_display = ("user_name", "city_name",)
