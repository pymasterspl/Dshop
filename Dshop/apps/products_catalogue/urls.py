from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import CeneoProductListView, ProductListView, \
    ProductDetailView, AddToCartView, CartDetailView, CategoryListView, CategoryDetailView, DeleteOneCartItemView, \
    DeleteCartItemView


urlpatterns = [
    path('products_list/', ProductListView.as_view(), name='products-list'),
    path('ceneo/', CeneoProductListView.as_view(), name='product-list'),
    path("products/<slug>-<int:id>/", ProductDetailView.as_view(), name='product-detail'),
    path("products/cart/add/<slug>/<int:id>/<str:quantity>/", AddToCartView.as_view(), name='add_to_cart'),
    path("products/cart/delete_one_cart_item/<slug>/<str:item_id>/<str:quantity>/", DeleteOneCartItemView.as_view(), name='delete_one_cart_item'),
    path("products/cart/delete_cart_item/<slug>/<str:id>/", DeleteCartItemView.as_view(), name='delete_cart_item'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('category/<slug>-<int:id>', CategoryDetailView.as_view(), name='category-detail'),
    path("cart_detail/", CartDetailView.as_view(), name='cart_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
