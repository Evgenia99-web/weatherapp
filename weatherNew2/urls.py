"""weatherNew2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from user import views as user_views
from weather import views
from django.conf.urls.i18n import i18n_patterns

router = routers.DefaultRouter()
router.register(r'cities', views.CityViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'stories', views.HistoryViewSet)
router.register(r'favorites', views.FavoriteViewSet)
router.register(r'weather', views.CurrentWeatherViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('edit_city_<str:city>/', user_views.edit_city, name='edit_city'),
    path('favorite_save_<str:city>/', user_views.favorite_go, name='favorite_go'),
    path('delete_<str:city>_<int:id>_hist/', user_views.delete_history_single, name='delete_history_single'),
    path('delete_all_history/', user_views.delete_history_all, name='delete_history_all'),
    path('delete_<str:city>_fav/', user_views.delete_favorite_single, name='delete_favorite_single'),
    path('delete_all_favorite/', user_views.delete_favorite_all, name='delete_favorite_all'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('', include('weather.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('router/', include(router.urls), name='router'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('edit_city_<str:city>/', user_views.edit_city, name='edit_city'),
    path('favorite_save_<str:city>/', user_views.favorite_go, name='favorite_go'),
    path('delete_<str:city>_<int:id>_hist/', user_views.delete_history_single, name='delete_history_single'),
    path('delete_all_history/', user_views.delete_history_all, name='delete_history_all'),
    path('delete_<str:city>_fav/', user_views.delete_favorite_single, name='delete_favorite_single'),
    path('delete_all_favorite/', user_views.delete_favorite_all, name='delete_favorite_all'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('', include('weather.urls')),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)