# Generated by Django 4.2.6 on 2023-12-04 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_room_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='username',
            field=models.CharField(default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
