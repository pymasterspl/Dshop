from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import CustomUser
from .serializers import RegistrationSerializer

User = get_user_model()


class RegistrationViewSet(mixins.CreateModelMixin, viewsets.ViewSet):
    """
    API Viewset responsible for single user registration

    :accepts: User model [username, email] + password1, password2
    :returns: 201 / 400
    """
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)
    throttle_scope = 'registration'

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password1']
            )
        except IntegrityError:
            user = None

        if user:
            custom_user = CustomUser(user=user)
            custom_user.save()
            content = {'detail': _('Registration success.')}
            return Response(content, status=status.HTTP_201_CREATED)
        else:
            content = {'detail': _('Unable to finish registration.')}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)