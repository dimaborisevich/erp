from django.urls import path, include

urlpatterns = [
    path('registration/', include('apps.registration.urls')),
]