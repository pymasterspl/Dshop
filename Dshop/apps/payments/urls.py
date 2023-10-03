from django.urls import path

from .views import PurchaseView, stripe_config, create_checkout_session

urlpatterns = [
    path('', PurchaseView.as_view(), name='purchase'),
    path('config/', stripe_config),
    path('create-checkout-session/', create_checkout_session),
]
