from django.urls import path

from .views import PurchaseView, SuccessView, CancelledView, CreateCheckoutSessionView, StripeWebhookView, \
    StripeConfigView

urlpatterns = [
    path('', PurchaseView.as_view(), name='purchase'),
    path('config/', StripeConfigView.as_view(), name='stripe_config'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('success/', SuccessView.as_view(), name='payment_success'),
    path('cancelled/', CancelledView.as_view(), name='payment_cancelled'),
    path('webhook/', StripeWebhookView.as_view(), name='stripe_webhook'),
]
