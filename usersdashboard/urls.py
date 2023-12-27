from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
  path('usercarehomeslist/',CareHomeListView.as_view(),name='usercarehomelisview'),
  path('userpersonslist/',PersonsListView.as_view(),name='userpersonslisview'),
  path('carehomesingleview/<int:pk>',CareHomeSingleView.as_view(),name='carehomesingleview'),
  path('personsingleview/<int:pk>',PersonSingleView.as_view(),name='personsingleview'),
  path('time-slots/<int:professional_id>/<str:date>/', TimeSlotListAPIView.as_view(), name='time-slot-list'),
  path('bookings/',BookingCreateAPIView.as_view(),name='booking-create'),
  path('user-bookings/', UserBookingListView.as_view(), name='user-bookings'),
  path('start_payment/<int:id>/', StartPaymentAPIView.as_view(), name='start_payment'),
  path('handle_payment_success/', HandlePaymentSuccessView.as_view(), name='handle_payment_success'),
  path('userbookingdistroy/<int:pk>/',UserBookingDestroyView.as_view(),name='userbookingdistroy'),
    
 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 