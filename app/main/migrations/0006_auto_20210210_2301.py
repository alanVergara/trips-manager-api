# Generated by Django 3.1.6 on 2021-02-11 02:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210210_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='passenger',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seats_passenger', to=settings.AUTH_USER_MODEL),
        ),
    ]
