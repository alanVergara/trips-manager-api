# Generated by Django 3.1.6 on 2021-02-10 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_route_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='driver',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
