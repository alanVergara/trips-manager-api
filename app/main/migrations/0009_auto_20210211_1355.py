# Generated by Django 3.1.6 on 2021-02-11 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_trip_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seat',
            name='passenger',
        ),
        migrations.RemoveField(
            model_name='seat',
            name='reserved',
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reserved', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets_admin', to=settings.AUTH_USER_MODEL)),
                ('passenger', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets_passenger', to=settings.AUTH_USER_MODEL)),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets_seat', to='main.seat')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets_trip', to='main.trip')),
            ],
        ),
    ]
