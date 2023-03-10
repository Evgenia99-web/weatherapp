# Generated by Django 4.1.5 on 2023-01-23 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(default='Набережные Челны', max_length=100, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(default='Россия', max_length=100, verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.CharField(default='Иван', max_length=100, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(default='Иванов', max_length=100, verbose_name='Фамилия'),
        ),
    ]
