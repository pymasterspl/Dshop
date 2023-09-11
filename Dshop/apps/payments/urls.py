from django.urls import path

from .views import PurchaseView

urlpatterns = [
    path('', PurchaseView.as_view(), name='purchase'),
]
