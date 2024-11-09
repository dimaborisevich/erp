from django.urls import path
from apps.registration.views import (
    UserProfileUpdateView,
    UserRegistrationView, 
    UserLoginView,
    AdminAccountManagerListView,
) 

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profileupdate/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('admins-managers/', AdminAccountManagerListView.as_view(), name='admins-managers')
]