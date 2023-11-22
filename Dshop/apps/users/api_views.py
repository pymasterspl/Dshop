from django.contrib.auth import get_user_model
from django.contrib.auth import login as django_login
from rest_framework import viewsets, mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import CustomUser
from .serializers import RegistrationSerializer, LoginSerializer, TokenSerializer

User = get_user_model()


class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API Viewset responsible for single user registration

    :accepts: User model [username, email] + password1, password2
    :returns: 201 / 400
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    throttle_scope = 'registration'
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        custom_user = CustomUser(user=user)
        custom_user.save()


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    throttle_scope = 'login'

    def post(self, request):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        django_login(request, user)

        token, _ = Token.objects.get_or_create(user=user)
        token_serializer = TokenSerializer(instance=token)
        return Response(token_serializer.data, status=status.HTTP_200_OK)
