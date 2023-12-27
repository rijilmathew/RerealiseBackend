from django.forms import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from authentification.models import User,UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','password', 'is_staff', 'is_active','is_service_provider' , 'is_superuser', 'mobile_number') 

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'dob', 'address_lane_1', 'address_lane_2', 'pincode', 'profile_photo')


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','password', 'is_staff', 'is_active','is_service_provider' , 'is_superuser', 'mobile_number') 






class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user']={
            'userId':user.id,
            'username':user.username,
            'email':user.email,
            'password':user.password,
            'mobile_number':user.mobile_number,
            'is_active':user.is_active,
            'is_staff':user.is_staff,
            'is_superuser':user.is_superuser,
            'is_service_provider':user.is_service_provider,
        }
        return token
    




class ServiceProviderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        exclude = ('id','user')