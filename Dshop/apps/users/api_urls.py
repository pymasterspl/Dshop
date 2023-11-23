from django.urls import path

from .api_views import RegistrationViewSet, LoginView

urlpatterns = [
    path('register/', RegistrationViewSet.as_view({'post': 'create'}), name='api-register'),
    path('login/', LoginView.as_view(), name='api-login'),
]

