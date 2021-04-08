from rest_framework import serializers
from .models import Shoe, User, Review, Size, Order, OrderItem, Shipping, Review

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('size',)

class ShoeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoe
        fields = '__all__'

class ShoeSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoe
        fields = ['catalogue_code', 'name', 'collection', 'price', 'shoe_image']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["customer", "date_ordered", "completed", "transaction_id"]

class OrderItemSerializer(serializers.ModelSerializer):
    shoe_name = serializers.CharField(source='shoe.name')
    shoe_collection = serializers.CharField(source='shoe.collection')
    shoe_catalogue_code = serializers.CharField(source='shoe.catalogue_code')
    shoe_price = serializers.CharField(source='shoe.price')
    shoe_image = serializers.ImageField(source='shoe.shoe_image')
    class Meta:
        model = OrderItem
        fields = ["order", "quantity", "size", "shoe_name", "shoe_collection", "shoe_catalogue_code", "shoe_price", "shoe_image"]

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

