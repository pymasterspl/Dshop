from django.urls import path
from .views import RegistrationView, LoginUserView, LogoutView, HomeView, \
    RemoveUserView, UpdateUserView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete-user/', RemoveUserView.as_view(), name='delete_user'),
    path('update-user/', UpdateUserView.as_view(), name='update_user')
]



