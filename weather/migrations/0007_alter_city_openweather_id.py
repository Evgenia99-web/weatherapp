# Generated by Django 4.1.5 on 2023-01-24 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0006_alter_city_openweather_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='openweather_id',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
