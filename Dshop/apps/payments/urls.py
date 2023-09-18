from django.urls import path

from .views import PurchaseView, stripe_config

urlpatterns = [
    path('', PurchaseView.as_view(), name='purchase'),
    path('config/', stripe_config),
]
