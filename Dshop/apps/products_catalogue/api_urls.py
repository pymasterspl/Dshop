from django.urls import path
from .api_views import CartAPIView


urlpatterns = [
    path("add/<int:id>/<int:quantity>/", CartAPIView.as_view(), name="api_add_to_cart"),
    path("delete/<str:item_id>/<int:quantity>/", CartAPIView.as_view(), name="api_delete_cart_items"),
    path("delete/<str:item_id>/", CartAPIView.as_view(), name="api_delete_all_cart_items"),
    path("detail/", CartAPIView.as_view(), name="api_cart_detail"),
]