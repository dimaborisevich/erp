from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from apps.registration.serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer,
    UserProfileUpdateSerializer,
    UserListSerializer,
    ChangePasswordSerializer,
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
    

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class=ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({"old_password": "Неверный текущий пароль"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({"detail": "Пароль успешно изменен"}, status=status.HTTP_200_OK)
    

class DeleteAdminManagerView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def delete(self,request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user_to_delete = self.get_queryset().filter(pk=user_id).first()

        if not user_to_delete:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        if user_to_delete.role.name not in ['Суперадмин', 'Аккаунт-менеджер']:
            return Response({"detail": "Вы можете удалять только аккаунт-менеджеров или суперадминов"}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.role.name != "Суперадмин":
            return Response({"detail": "Доступ запрещен. Только суперадмины могут удалять учетные записи."}, status=status.HTTP_403_FORBIDDEN)
        
        user_to_delete.delete()
        return Response({"detail": "Пользователь успешно удален"}, status=status.HTTP_200_OK)