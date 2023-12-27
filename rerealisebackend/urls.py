from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import ( TokenRefreshView,TokenVerifyView)
from authentification.views import MyTokenObtainPairView
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', MyTokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view()),
    path('api/authentification/',include('authentification.urls')),
    path('api/usersdashboard/',include('usersdashboard.urls')),
    path('api/admindashboard/',include('admindashboard.urls')),
    path('api/providerdashboard/',include('providerdashboard.urls')),
    path('api/chat/',include('chat.urls')),
    path('auth/',include('drf_social_oauth2.urls',namespace='drf')),

    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
