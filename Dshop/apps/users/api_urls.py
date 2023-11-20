from django.urls import path
from .api_views import RegistrationView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='api-registration'),
]

