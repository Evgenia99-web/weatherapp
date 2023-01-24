from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:city_name>-<int:city_openweather_id>/', views.city_detail, name='city_detail'),
]
