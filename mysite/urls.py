from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('user_auth.urls')),
    path('', include('contact_app.urls')), 
    path('admin/', admin.site.urls),
]