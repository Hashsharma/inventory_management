from rest_framework import serializers
from .models import Product, Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'product_quantity_in_stock', 'product_price']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'order_quantity', 'order_date', 'order_status', 'order_total_price']
        read_only_fields = ['order_date', 'order_total_price']
