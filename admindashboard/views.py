from django.shortcuts import render
from rest_framework import generics,permissions,status
from authentification.serializers import UserSerializer
from .serializers import *
from authentification.models import *
from django.db.models import Q
from providerdashboard.serializers import CareHomeSerializer,PersonSerializer
from providerdashboard.models import CareHome,ProfessionalPerson
from rest_framework.response import Response

# Create your views here.
class UserListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter((Q( is_service_provider=False) & Q(is_superuser=False)))
        return queryset
    

class UserBlockView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserBlockSerializer
    lookup_field = 'id'  # assuming you're using 'id' as the lookup field for users

  


class UserUnblockView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUnblockSerializer
    lookup_field = 'id'  # assuming you're using 'id' as the lookup field for users


class ProviderListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter((Q( is_service_provider=True) & Q(is_superuser=False)))
        return queryset

 
class CareHomeListView(generics.ListAPIView):
    serializer_class = CareHomeSerializer

    def get_queryset(self):
        queryset= CareHome.objects.filter(is_active=False)
        return queryset

class CareHomeUpdateApiView(generics.RetrieveUpdateAPIView):
    queryset = CareHome.objects.all()
    serializer_class = CareHomeSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PersonListView(generics.ListAPIView):
    serializer_class = PersonSerializer

    def get_queryset(self):
        queryset= ProfessionalPerson.objects.filter(is_active=False)
        return queryset
    


class PersonUpdateApiView(generics.RetrieveUpdateAPIView):
    queryset = ProfessionalPerson.objects.all()
    serializer_class = PersonSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProviderCountView(generics.RetrieveAPIView):
    serializer_class=UserCountSerializer

    def retrieve(self, request, *args, **kwargs):
        user_count=User.objects.filter(is_staff=False, is_service_provider=False).count()
        provider_count=User.objects.filter(is_service_provider=True).count()

        data = {'user_count': user_count, 'provider_count': provider_count}
        serializer = self.get_serializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ServicesCountView(generics.RetrieveAPIView):
    serializer_class=ServicesCountSerializer

    def retrieve(self, request, *args, **kwargs):
        carehome_count=CareHome.objects.filter(is_active=True).count()
        person_count=ProfessionalPerson.objects.filter(is_active=True).count()

        data = {'carehome_count': carehome_count, 'person_count': person_count}
        serializer = self.get_serializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)