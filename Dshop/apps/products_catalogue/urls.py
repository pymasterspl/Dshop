from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import CeneoCategoriesView, CeneoProductListView, ProductListView, \
    ProductDetailView, AddToCartView, CartDetailView, CategoryListView, CategoryDetailView, DeleteOneCartItemView, \
    DeleteCartItemView,


urlpatterns = [
    path('products_list/', ProductListView.as_view(), name='products-list'),
    path('ceneo/', CeneoProductListView.as_view(), name='product-list'),
    path('ceneo_categories/', CeneoCategoriesView.as_view(), name='ceneo-categories'),
    path("products/<slug>-<int:id>", ProductDetailView.as_view(), name='product-detail'),
    path("products/cart/add/<slug>/<int:id>", AddToCartView.as_view(), name='add_to_cart_view'),
    path("products/cart/delete_one_cart_item/<slug>/<str:item_id>", DeleteOneCartItemView.as_view(), name='delete_one_cart_item_view'),
    path("products/cart/delete_cart_item/<slug>/<str:id>", DeleteCartItemView.as_view(), name='delete_cart_item_view'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('category/<slug>-<int:id>', CategoryDetailView.as_view(), name='category-detail'),
    path("cart_detail/", CartDetailView.as_view(), name='cart_detail_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
