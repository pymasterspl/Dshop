from django.urls import path

from .views import PurchaseView, SuccessView, CancelledView, stripe_config, create_checkout_session, stripe_webhook

urlpatterns = [
    path('', PurchaseView.as_view(), name='purchase'),
    path('config/', stripe_config, name='stripe_config'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('success/', SuccessView.as_view(), name='payment_success'),
    path('cancelled/', CancelledView.as_view(), name='payment_cancelled'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
]
