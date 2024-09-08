from django.urls import path, include

urlpatterns = [
    path('', include('apps.registration.urls')),
]