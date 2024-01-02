from django.urls import path

from .views import InPostShippingView, PaczkomatPageView, HandleMethodChoiceView, InPostSendingMethodView

urlpatterns = [
    path('', InPostShippingView.as_view(), name='shipping-page'),
    path('paczkomat/', PaczkomatPageView.as_view(), name='paczkomat-page'),
    path('shipping-choice/', HandleMethodChoiceView.as_view(), name='handle-method-choice'),
    path('sending-methods/', InPostSendingMethodView.as_view(), name='sending-methods'),
]
