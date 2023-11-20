from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import AllowAny
# from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    """
    API View responsible for single user registration

    :accepts: default Django User model fields (django.contrib.auth.models.User) [username, email, password1, password2]
    :returns: 201 / 400
    """
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    throttle_scope = 'registration'

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.get_cleaned_data()

        # Try to create new object instance with the validated data of username and email
        try:
            user = User.objects.create_user(
                username=cleaned_data['username'],
                email=cleaned_data['email'],
                password=cleaned_data['password']
            )
        except IntegrityError:
            user = None

        if user:
            # finish registration
            custom_user = CustomUser(user=user)  # I really don't like this. It should be signals
            custom_user.save()
            content = {'detail': _('Registration success.')}
            return Response(content, status=status.HTTP_201_CREATED)
        else:
            content = {'detail': _('Unable to finish registration.')}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)