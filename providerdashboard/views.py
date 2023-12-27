from django.shortcuts import render
from rest_framework import generics
from authentification.serializers import UserSerializer
from .models import *
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
from usersdashboard.pagination import StandardResultsSetPagination
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
# Create your views here.


class CareHomeListCreateAPIView(generics.ListCreateAPIView):
    parser_classes = (MultiPartParser, FormParser)

    queryset=CareHome.objects.all()
    serializer_class=CareHomeSerializer
    pagination_class = StandardResultsSetPagination

class CareHomeProviderListView(generics.ListAPIView):
    serializer_class=CareHomeSerializer

    def get_queryset(self):
        provider_id = self.kwargs['provider_id']
        return CareHome.objects.filter(provider_id=provider_id)


class CareHomeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset = CareHome.objects.all()
    print('hai vannu')

    def get_serializer_class(self):
        # Use CareHomeUpdateSerializer for updates
        if self.request.method == 'PUT':
            return CareHomeUpdateSerializer
        # Use CareHomeSerializer for other methods
        return CareHomeSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        # Validate the serializer before accessing validated_data
        serializer.is_valid(raise_exception=True)

        # Check if 'imageone' is not in request.data or is None
        if 'imageone' not in request.data or request.data['imageone'] is None:
            # If 'imageone' is not provided or is None, remove it from data to avoid validation errors
            serializer.validated_data.pop('imageone', None)

        # Now you can safely access serializer.validated_data
        self.perform_update(serializer)
        return Response(serializer.data)




class PersonListCreateAPIView(generics.ListCreateAPIView):
    parser_classes = (MultiPartParser, FormParser)

    queryset=ProfessionalPerson.objects.all()
    serializer_class=PersonSerializer



class PersonProviderListView(generics.ListAPIView):
    serializer_class=PersonSerializer

    def get_queryset(self):
        provider_id = self.kwargs['provider_id']
        return ProfessionalPerson.objects.filter(provider_id=provider_id)

class PersonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset = ProfessionalPerson.objects.all()

    def get_serializer_class(self):
        # Use PersonUpdateSerializer for updates
        if self.request.method == 'PUT':
            return PersonUpdateSerializer
        # Use CareHomeSerializer for other methods
        return PersonSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        # Validate the serializer before accessing validated_data
        serializer.is_valid(raise_exception=True)

        # Check if 'imageone' is not in request.data or is None
        if 'profileimage' not in request.data or request.data['profileimage'] is None:
            # If 'imageone' is not provided or is None, remove it from data to avoid validation errors
            serializer.validated_data.pop('profileimage', None)

        # Now you can safely access serializer.validated_data
        self.perform_update(serializer)
        return Response(serializer.data)


class TimeSlotListCreateView(generics.ListCreateAPIView):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer


class TimeSlotUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset=TimeSlot.objects.all()
    serializer_class=TimeSlotSerializer

class TimeSlotStatusUpdateView(generics.UpdateAPIView):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotUpdateSerializer
    permission_classes = [IsAuthenticated]
    

class TimeSlotsForDateView(generics.ListAPIView):
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        date_param = self.kwargs.get('date')  # Assuming the date is passed as a URL parameter
        professional_id = self.kwargs.get('professional_id')

        if date_param:
            # Parse the date parameter to a Python date object
            try:
                parsed_date = datetime.strptime(date_param, '%Y-%m-%d').date()
                # Filter TimeSlots based on the provided date
                queryset = TimeSlot.objects.filter(date=parsed_date,professional=professional_id, is_booked=False)
            except ValueError:
                # Handle invalid date format
                queryset = TimeSlot.objects.none()
        else:
            # If no date is provided, return an empty queryset
            queryset = TimeSlot.objects.none()

        return queryset



class ProviderBookingListView(generics.ListAPIView):
    serializer_class = BookingViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the provider ID from the request data
        provider_id = self.request.query_params.get('provider_id')

        # Assuming the logged-in user is a provider
        provider_bookings = Booking.objects.filter(timeslot__provider_id=provider_id).order_by('-date', '-timeslot__start_time')

       
        return provider_bookings
    


class BookingNotificationListCreateView(generics.ListCreateAPIView):
    queryset =BookingNotification.objects.all()
    serializer_class = BookingNotificationSerializer
    

class BookingNotificationListView(generics.ListAPIView):
    serializer_class = BookingNotificationSerializer

    def get_queryset(self):
        provider_id = self.kwargs['provider_id']
        return BookingNotification.objects.filter(provider_id=provider_id, read_status=False)
    

class MarkNotificationsAsReadView(generics.UpdateAPIView):
    queryset = BookingNotification.objects.all()
    serializer_class = BookingNotificationSerializer

    def update(self, request, *args, **kwargs):
        provider_id = kwargs.get('provider_id')
        notifications = BookingNotification.objects.filter(provider=provider_id, read_status=False)

        for notification in notifications:
            notification.read_status = True
            notification.save()

        return Response({'detail': 'Notifications marked as read successfully.'}, status=status.HTTP_200_OK)
    
class CareHomeReviewListCreateView(generics.ListCreateAPIView):
    queryset=CareHomeReview.objects.all()
    serializer_class=CareHomeReviewSerializer

class CareHomeReviewListView(generics.ListAPIView):
    serializer_class=CareHomeReviewSerializer

    def get_queryset(self):
        careHome_id=self.kwargs.get('careHome_id')
        return CareHomeReview.objects.filter(CareHome_id=careHome_id,is_block=False)
    
class CareHomeReviewBlockView(generics.RetrieveUpdateAPIView):
    queryset = CareHomeReview.objects.all()
    serializer_class = CareHomeReviewBlockSerializer
    lookup_field = 'id' 

class CareHomeReviewUnblockView(generics.RetrieveUpdateAPIView):
    queryset = CareHomeReview.objects.all()
    serializer_class = CareHomeReviewUnblockSerializer
    lookup_field = 'id' 
    
class ProfessionalPersonReviewListCreateView(generics.ListCreateAPIView):
    queryset=ProfessionalPersonReview.objects.all()
    serializer_class=ProfessionalPersonReviewSerializer

class ProfessionalPersonReviewListView(generics.ListAPIView):
    serializer_class=ProfessionalPersonReviewSerializer

    def get_queryset(self):
        ProfessionalPerson_id=self.kwargs.get('ProfessionalPerson_id')
        return ProfessionalPersonReview.objects.filter(ProfessionalPerson_id=ProfessionalPerson_id)
    
class ProfessionalsReviewBlockView(generics.RetrieveUpdateAPIView):
    queryset = ProfessionalPersonReview.objects.all()
    serializer_class = ProfessionalsReviewBlockSerializer
    lookup_field = 'id' 


class ProfessionalsReviewUnblockView(generics.RetrieveUpdateAPIView):
    queryset = ProfessionalPersonReview.objects.all()
    serializer_class = ProfessionalsReviewUnblockSerializer
    lookup_field = 'id' 