from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

import weather.models
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CityUpdateForm
from .models import History, Favorite
from weather.models import City


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    contact_list = City.objects.all()
    paginator = Paginator(contact_list, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'histories': History.objects.filter(user_name=request.user).order_by("-id"),
        'favorites': Favorite.objects.filter(user_name=request.user).order_by("-id"),
        'page_obj': page_obj,
        'countries': City.objects.values("country_code").distinct(),
    }

    return render(request, 'profile.html', context)


def edit_city(request, city):
    city_model = City.objects.get(name=city)
    c_form = CityUpdateForm(request.GET, request.FILES, instance=city_model)
    if request.method == 'POST':
        c_form = CityUpdateForm(request.POST, request.FILES, instance=city_model)
        if c_form.is_valid():
            c_form.save()
            messages.success(request, f'Данные города успешно обновлен.')
            return redirect('profile')
        else:
            c_form = CityUpdateForm(instance=city_model)
            messages.get_messages(request)

    context = {
        'c_form': c_form,
        'city': city
    }

    return render(request, 'edit_city.html', context)


def favorite_go(request, city):
    current_city = City.objects.get(name=city)
    if not Favorite.objects.filter(city_name=current_city):
        fav_city = Favorite(
            city_name=City.objects.get(name=city),
            user_name=request.user,
        )
        fav_city.save()
        fav = True
    else:
        Favorite.objects.filter(city_name=current_city).delete()
        fav = False

    context = {
        'city': city,
        'favorite': fav
    }
    return render(request, 'favorite_save.html', context)


def delete_history_single(request, city, id):
    current_city = City.objects.get(name=city)
    History.objects.filter(pk=id).delete()

    del_hist = {
        'id': id,
        'city': current_city
    }
    return render(request, 'delete_single_hist.html', del_hist)


def delete_history_all(request):
    current_user = request.user
    History.objects.filter(user_name=current_user).delete()
    return render(request, 'delete_all_hist.html')


def delete_favorite_single(request, city):
    current_city = City.objects.get(name=city)
    Favorite.objects.filter(city_name=current_city, user_name=request.user).delete()

    del_hist = {
        'city': current_city
    }
    return render(request, 'delete_single_fav.html', del_hist)


def delete_favorite_all(request):
    current_user = request.user
    Favorite.objects.filter(user_name=current_user).delete()
    return render(request, 'delete_all_fav.html')

