from django.urls import path

from .api_views import RegistrationViewSet, LoginView, LogoutView, PasswordChangeView, UserDataChangeView

urlpatterns = [
    path('register/', RegistrationViewSet.as_view({'post': 'create'}), name='api-register'),
    path('login/', LoginView.as_view(), name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout'),
    path('password/change/', PasswordChangeView.as_view(), name='api-password-change'),
    path('', UserDataChangeView.as_view({'get': 'retrieve', 'patch': 'update'}), name='api-user-details'),
]

