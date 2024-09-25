from django.urls import path
from .views import product_list, product_detail, product_add
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('items/add', product_add, name='product_add'),
    path('items/all', product_list, name='product_list'),
    path('items/<int:product_id>', product_detail, name='product_detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)