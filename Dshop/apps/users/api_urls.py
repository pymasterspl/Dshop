from django.urls import path
from .api_views import RegistrationViewSet

urlpatterns = [
    path('register/', RegistrationViewSet.as_view({'post': 'create'}), name='api-register'),
]

