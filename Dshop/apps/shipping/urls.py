from django.urls import path

from .views import InPostSendingMethodsView, PaczkomatPageView, HandleMethodChoiceView

urlpatterns = [
    path('', InPostSendingMethodsView.as_view(), name='shipping_methods'),
    path('paczkomat/', PaczkomatPageView.as_view(), name='paczkomat_page'),
    path('shipping-method/', HandleMethodChoiceView.as_view(), name='handle_method_choice')
]
