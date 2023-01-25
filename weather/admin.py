from django.contrib import admin
from .models import City, CurrentWeather, CityStats, StatsSummary


# admin.site.register(City)
# admin.site.register(CurrentWeather)
# admin.site.register(CityStats)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "openweather_id", "latitude", "longitude",)
    search_fields = ("name__icontains",)


@admin.register(CurrentWeather)
class CityAdmin(admin.ModelAdmin):
    # fields = ("city",)
    list_display = ("city", "temp", )


@admin.register(CityStats)
class CityAdmin(admin.ModelAdmin):
    list_display = ("city", "views",)
