import datetime

from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from weather.models import City


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField("Страна", max_length=100, default='Россия')
    city = models.CharField("Город", max_length=100, default='Набережные Челны')
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class History(models.Model):
    city_name = models.ForeignKey(City, on_delete=models.CASCADE)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    search_date = models.DateTimeField()

    class Meta:
        verbose_name = 'История запроса'
        verbose_name_plural = 'История запросов'

    def __str__(self):
        return str(self.city_name)


class Favorite(models.Model):
    city_name = models.ForeignKey(City, on_delete=models.CASCADE)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Любимый город'
        verbose_name_plural = 'Любимые города'

    def __str__(self):
        return str(self.city_name)