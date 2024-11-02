from rest_framework import serializers
from django.core.validators import MinValueValidator
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderCrateSerializer(serializers.Serializer):
    pass


class AddToCartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(required=True, validators=[MinValueValidator(1)])
    order_id = serializers.IntegerField(required=True, validators=[MinValueValidator(1)])
    product_id = serializers.IntegerField(required=True, validators=[MinValueValidator(1)])