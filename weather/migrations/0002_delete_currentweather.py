# Generated by Django 4.1.5 on 2023-01-24 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CurrentWeather',
        ),
    ]