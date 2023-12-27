from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views


urlpatterns = [
  path('user_registration/',views.UserRegistrationView.as_view(),name='user_registration'),
  path('user-profile/<int:user_id>/', views.UserProfileView.as_view(), name='user-profile'),
  path('service_provider_profile',views.ServiceProviderProfileView.as_view(),name='service_provider_profile'),

 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 