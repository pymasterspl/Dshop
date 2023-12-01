from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser
from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
    PasswordChangeSerializer,
    UserDataChangeSerializer,
    UserDataReadSerializer
)

User = get_user_model()


class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    throttle_scope = 'registration'
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        custom_user = CustomUser(user=user)
        custom_user.save()


class LoginView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer
    throttle_scope = 'login'

    def post(self, request):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        login(request, user)

        token, _ = Token.objects.get_or_create(user=user)
        if token:
            data = {
                "token": token.key,
                "username": user.username,
                "email": user.email
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            msg = {'detail': _('Unable to retrieve user auth token')}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(GenericAPIView):
    permission_classes = (AllowAny, )
    throttle_scope = 'logout'

    def get(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        logout(request)

        return Response(
            {'detail': _('Successfully logged out.')},
            status=status.HTTP_200_OK,
        )


class PasswordChangeView(GenericAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated, )
    throttle_scope = 'password_change'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'detail': _('New password has been saved.')}, status=status.HTTP_200_OK)


class UserDataChangeView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    throttle_scope = 'change_user_data'

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return UserDataChangeSerializer
        return UserDataReadSerializer

    def get_object(self):
        return CustomUser.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        request.data['user'] = self.request.user.id
        return super().update(request, *args, **kwargs)