from django.urls import path
from .api_views import CartAPIView


urlpatterns = [
    path("", CartAPIView.as_view(), name="api_cart")
]