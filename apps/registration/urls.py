from django.urls import path
from apps.registration.views import (
    UserProfileUpdateView,
    UserRegistrationView, 
    UserLoginView,
    AdminListView,
    ManagerListView,
) 

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profileupdate/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('admins-list/', AdminListView.as_view(), name='admins-list'),
    path('managers-list/', ManagerListView.as_view(), name='managers-list')
]