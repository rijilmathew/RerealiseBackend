# Generated by Django 4.2.6 on 2023-10-15 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField(null=True)),
                ('address_lane_1', models.CharField(max_length=300)),
                ('address_lane_2', models.CharField(max_length=300)),
                ('pincode', models.CharField(max_length=50)),
                ('profile_photo', models.ImageField(upload_to='UserProfile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceProviderProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField(null=True)),
                ('address_lane_1', models.CharField(max_length=300)),
                ('address_lane_2', models.CharField(max_length=300)),
                ('pincode', models.CharField(max_length=50)),
                ('profile_photo', models.ImageField(upload_to='ProviderProfile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
