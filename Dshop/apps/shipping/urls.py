from django.urls import path

from .views import InPostSendingMethodsView

urlpatterns = [
    path('', InPostSendingMethodsView.as_view(), name='shipping_methods'),
]