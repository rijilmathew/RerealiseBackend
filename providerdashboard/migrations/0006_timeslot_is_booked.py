# Generated by Django 4.2.6 on 2023-11-14 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providerdashboard', '0005_timeslot_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='is_booked',
            field=models.BooleanField(default=False),
        ),
    ]
