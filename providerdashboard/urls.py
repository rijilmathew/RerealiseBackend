from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('carehomes/', CareHomeListCreateAPIView.as_view(), name='carehome-list-create'),  # List and Create
    path('carehomes/<int:pk>', CareHomeDetailAPIView.as_view(), name='carehome-detail'),  # Retrieve, Update, Destroy
    path('provider-carehomes/<int:provider_id>', CareHomeProviderListView.as_view(), name='providercarehome-detail'), 
    path('persons/', PersonListCreateAPIView.as_view(), name='person-list-create'),  # List and Create
    path('persons/<int:pk>', PersonDetailAPIView.as_view(), name='person-detail'),
    path('provider-persons/<int:provider_id>', PersonProviderListView.as_view(), name='providerperson-detail'),
    path('addtimeslot/',TimeSlotListCreateView.as_view(),name='add-timeslot'),
    path('time-slots/<str:date>/<int:professional_id>/', TimeSlotsForDateView.as_view(), name='time-slots-for-date-and-professional'),
    path('time-slots/<int:pk>', TimeSlotUpdateView.as_view(), name='update-timeslot'),
    path('provider-bookings/', ProviderBookingListView.as_view(), name='provider-bookings'),
    path('booking-notification/',BookingNotificationListCreateView.as_view(),name='booking-notification'),
    path('booking-notifications/<int:provider_id>/', BookingNotificationListView.as_view(), name='booking-notifications-list'),
    path('mark-notifications-as-read/<int:provider_id>/', MarkNotificationsAsReadView.as_view(), name='mark-notifications-as-read'),
    path('updatetimeSlot/<int:pk>/', TimeSlotStatusUpdateView.as_view(), name='update-timeslot'),
    path('carehome-review/',CareHomeReviewListCreateView.as_view(),name='carehome-review'),
    path('carehome-review/<int:careHome_id>/',CareHomeReviewListView.as_view(),name='carehome-review-list'),
    path('carehomereview-block/<int:id>/', CareHomeReviewBlockView.as_view(), name='carehomereview-block'),
    path('carehomereview-unblock/<int:id>/', CareHomeReviewUnblockView.as_view(), name='carehomereview-unblock'),
    path('persons-review/',ProfessionalPersonReviewListCreateView.as_view(),name='persons-review'),
    path('persons-review/<int:ProfessionalPerson_id>/',ProfessionalPersonReviewListView.as_view(),name='persons-review-list'),
    path('professionalsreview-block/<int:id>/', ProfessionalsReviewBlockView.as_view(), name='professionalsreview-block'),
    path('professionalsreview-unblock/<int:id>/', ProfessionalsReviewUnblockView.as_view(), name='professionalsreview-unblock'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 