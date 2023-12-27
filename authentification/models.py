from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email=models.EmailField(max_length=50,unique=True)
    is_service_provider = models.BooleanField(default=False)
    mobile_number = models.CharField(max_length=10, null=True, blank=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['mobile_number','username']


    def __str__(self):
        return self.username
    


class UserProfile(models.Model):
    
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    dob=models.DateField(null=True)
    address_lane_1=models.CharField(max_length=300)
    address_lane_2=models.CharField(max_length=300)
    pincode=models.CharField(max_length=50)
    profile_photo=models.ImageField(upload_to='UserProfile')

    def __str__(self):
        return self.user.username
    

class ServiceProviderProfile(models.Model):
    
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    dob=models.DateField(null=True)
    address_lane_1=models.CharField(max_length=300)
    address_lane_2=models.CharField(max_length=300)
    pincode=models.CharField(max_length=50)
    profile_photo=models.ImageField(upload_to='ProviderProfile')

    def __str__(self):
        return self.user.username
    