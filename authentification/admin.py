from django.contrib import admin

# Register your models here.
from .models import User,UserProfile,ServiceProviderProfile


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(ServiceProviderProfile)