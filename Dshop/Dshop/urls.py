"""
URL configuration for Dshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from sitemap import ProductSitemap, StaticViewSitemap, CategorySitemap

sitemaps ={
    'products' : ProductSitemap,
    'categories': CategorySitemap,
    "static": StaticViewSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap",
    ),
    path('products/', include('apps.products_catalogue.urls')),
    path('payments/', include('apps.payments.urls')),
    path('shipping/', include('apps.shipping.urls')),
    path('users/', include('apps.users.urls')),
    path('tinymce/', include('tinymce.urls')),

    path('api/users/', include('apps.users.api_urls')),
    path('api/products/', include('apps.products_catalogue.api_urls')),

    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
 ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
