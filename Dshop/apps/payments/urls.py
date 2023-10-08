from django.urls import path

from .views import PurchaseView, SuccessView, CancelledView, stripe_config, create_checkout_session, stripe_webhook

urlpatterns = [
    path('', PurchaseView.as_view(), name='purchase'),
    path('config/', stripe_config),
    path('create-checkout-session/', create_checkout_session),
    path('success/', SuccessView.as_view()),
    path('cancelled/', CancelledView.as_view()),
    path('webhook/', stripe_webhook),
]
