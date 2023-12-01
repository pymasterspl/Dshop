from django.urls import path

from .api_views import RegistrationViewSet, LoginView, LogoutView, PasswordChangeView, UserDataChangeView

urlpatterns = [
    path('', UserDataChangeView.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'update'}
    ),
         name='api-user-details'
         ),
    path('register/', RegistrationViewSet.as_view({'post': 'create'}), name='api-register'),
    path('login/', LoginView.as_view(), name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout'),
    path('password/change/', PasswordChangeView.as_view(), name='api-password-change'),
]

