from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
  path('users-list/',UserListView.as_view(),name='user-list'),
  path('user-block/<int:id>/', UserBlockView.as_view(), name='user-block'),
  path('user-unblock/<int:id>/', UserUnblockView.as_view(), name='user-unblock'),
  path('provider-list/',ProviderListView.as_view(), name='user-list'),
  path('carehomelist/',CareHomeListView.as_view(),name='carehomelistview'),
  path('carehomelist/<int:pk>/',CareHomeUpdateApiView.as_view(),name='carehomelist'),
  path('personlist/',PersonListView.as_view(),name='personlistview'),
  path('personlist/<int:pk>/',PersonUpdateApiView.as_view(),name='personlist'),
  path('user-provider-count/', UserProviderCountView.as_view(), name='user-provider-count'),
  path('services-count/', ServicesCountView.as_view(), name='services-count'),
  
  
 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 