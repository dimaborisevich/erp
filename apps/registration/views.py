from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from apps.registration.serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer,
    UserProfileUpdateSerializer,
    UserListSerializer,
)
from apps.registration.permissions import IsSuperAdminOrAccountManager
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),                
            },
            status=status.HTTP_201_CREATED,
        )

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'], 
            password=serializer.validated_data['password']
        )
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "role": user.role.name if user.role else None, 
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        


class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperAdminOrAccountManager]

    def get_object(self):
        return self.request.user


class AdminListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [AllowAny] 

    def get_queryset(self):
        return User.objects.filter(role__name__in=['Суперадмин'])
    
class ManagerListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.filter(role__name__in=['Аккаунт-менеджер'])