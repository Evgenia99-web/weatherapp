# Generated by Django 4.1.5 on 2023-01-26 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0007_alter_city_openweather_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='image',
            field=models.ImageField(default='city_default.jpg', upload_to='city_pics'),
        ),
    ]
