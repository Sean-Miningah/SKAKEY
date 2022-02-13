from rest_framework import serializers

from .models import ProductCategory, ShopProduct, Shop
from .models import (ProductCategory,
                     ShopProduct, ShoppingSession, CartItem)
from payment.serializers import PaymentMethodSerializer

from django.contrib.auth import get_user_model
Shop = get_user_model()


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        exclude = ['is_staff', 'is_active', 'start_date']


class ShopRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = (
            "id", "first_name", "last_name", "shopname", "location", "photo",
            "category", "firebase_token", "phonenumber"
        )
        extra_kwargs = {"firebase_token": {"write_only": True}}

        def create(self, validated_data):
            password = validated_data.pop('firebase_token')
            shop = Shop(**validated_data)
            shop.save()
            return shop


class ShopProductCategorySerializer(serializers.ModelSerializer):
    shop = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.all(), many=False)

    class Meta:
        model = ProductCategory
        exclude = ['last_update']
        extra_kwargs = {"id": {"read_only": True}}


class ShopProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(), many=False)
    shop = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.all(), many=False)

    class Meta:
        model = ShopProduct
        exclude = ['date_created', 'last_update']
        extra_kwargs = {'id': {"read_only": True}}

class CartItemSerializer(serializers.ModelSerializer):
    session = serializers.PrimaryKeyRelatedField(
        queryset=ShoppingSession.objects.all, many=False)
    product = serializers.PrimaryKeyRelatedField(
        queryset=ShopProduct.objects.all(), many=False)

    class Meta:
        model = CartItem
        fields = (
            'session', 'product', 'quantity', 'price'
        )



class ShoppingSessionSerializer(serializers.ModelSerializer):

    shop = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.all(), many=False)

    class Meta:
        model = ShoppingSession
        fields = (
            'id', 'shop', 'created_at', 'total', 'payment_method'
        )
        extra_kwargs = {'total': {'required': False}}
        
        
class ReceiptSerializer(serializers.Serializer):
    
    # shopname = ShopSerializer()
    cart = ShoppingSessionSerializer()
    cartitems = CartItemSerializer(many=True)
    paymentmethod = PaymentMethodSerializer()

