# Generated by Django 4.1.5 on 2023-01-25 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0010_alter_history_city_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='user_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
