from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import  MyTokenObtainPairSerializer,ServiceProviderProfileSerializer,UserProfileSerializer,UserRegistrationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.hashers import make_password
from authentification.models import User,UserProfile,ServiceProviderProfile
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser




class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
   
    

class UserRegistrationView(generics.CreateAPIView):

    queryset=User.objects.all()
    serializer_class=UserRegistrationSerializer
    permission_classes=(AllowAny,)

    def perform_create(self, serializer):
        
        user = serializer.save()

        password = serializer.validated_data.get('password')
        hashed_password = make_password(password)
        user.password=hashed_password
        
        
        if user.is_staff == False and user.is_superuser == False:
            UserProfile.objects.create(user=user)
            user.save()
        elif user.is_staff == False and user.is_superuser == False:
            ServiceProviderProfile.objects.create(user=user)
            user.save()
        else:
            user.save()

class UserProfileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, user_id):
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request, user_id):
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


   

class ServiceProviderProfileView(generics.RetrieveUpdateAPIView):

    serializer_class=ServiceProviderProfileSerializer
    permission_classes=(IsAuthenticated,)
 
    try:
        def get_object(self):
            return self.request.user.ServiceProviderProfile
    except:
        print("Service Provider Profile not found")