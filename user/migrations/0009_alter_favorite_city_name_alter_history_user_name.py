# Generated by Django 4.1.5 on 2023-01-25 08:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('weather', '0007_alter_city_openweather_id'),
        ('user', '0008_alter_profile_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='city_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.city'),
        ),
        migrations.AlterField(
            model_name='history',
            name='user_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]