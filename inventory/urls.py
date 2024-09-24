from django.urls import path
from .views import product_list, product_detail, order_list, order_detail

urlpatterns = [
    path('items/all/', product_list, name='product_list'),
    path('items/<int:pk>/', product_detail, name='product_detail'),
    path('orders/', order_list, name='order_list'),
    path('orders/<int:pk>/', order_detail, name='order_detail'),
]
