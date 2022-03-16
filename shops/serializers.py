from rest_framework import serializers

from .models import (OTPAuthentication, Shop, County,
                     SubCounty, Ward, )
# from payment.serclearializers import PaymentMethodSerializer

from django.contrib.auth import get_user_model
ShopKeeper = get_user_model()


# class ShopSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Shop
#         exclude = ['is_staff', 'is_active', 'start_date']

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPAuthentication
        exclude = ['id',]

class ShopKeeperSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopKeeper
        exclude = ['is_staff','is_active','password']
        # extra_kwargs = {"firebase_token": {"write_only": True}}

        def create(self, validated_data):
            password = validated_data.pop('login_token')
            shop = Shop(**validated_data)
            shop.save()
            return shop
        
        
class AccountInfoSerializer(serializers.ModelSerializer):
    shop = serializers.StringRelatedField()
    
    class Meta:
        model = ShopKeeper
        exclude = ['is_staff','is_active','password']
        # extra_kwargs = {"firebase_token": {"write_only": True}}

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        exclude = ['confirmation_code',]

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County 
        fields = '__all__'
        
class SubCountySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCounty 
        fields = '__all__'
        
class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward 
        fields = '__all__'
        
class LocationOptionsSerializer(serializers.ModelSerializer):
    subcounties = SubCountySerializer(many=True)
    wards = WardSerializer(many=True)
    
    class Meta:
        model = County
        fields = ('id', 'name', 'subcounties', 'wards')
        




# class ShopProductCategorySerializer(serializers.ModelSerializer):
#     shop = serializers.PrimaryKeyRelatedField(
#         queryset=Shop.objects.all(), many=False)

#     class Meta:
#         model = ProductCategory
#         exclude = ['last_update']
#         extra_kwargs = {"id": {"read_only": True}}


# class ShopProductSerializer(serializers.ModelSerializer):
#     category = serializers.PrimaryKeyRelatedField(
#         queryset=ProductCategory.objects.all(), many=False)
#     shop = serializers.PrimaryKeyRelatedField(
#         queryset=Shop.objects.all(), many=False)

#     class Meta:
#         model = ShopProduct
#         exclude = ['date_created', 'last_update']
#         extra_kwargs = {'id': {"read_only": True}}

# class CartItemSerializer(serializers.ModelSerializer):
#     session = serializers.PrimaryKeyRelatedField(
#         queryset=ShoppingSession.objects.all, many=False)
#     product = serializers.PrimaryKeyRelatedField(
#         queryset=ShopProduct.objects.all(), many=False)

#     class Meta:
#         model = CartItem
#         fields = (
#             'session', 'product', 'quantity', 'price'
#         )



# class ShoppingSessionSerializer(serializers.ModelSerializer):

#     shop = serializers.PrimaryKeyRelatedField(
#         queryset=Shop.objects.all(), many=False)

#     class Meta:
#         model = ShoppingSession
#         fields = (
#             'id', 'shop', 'created_at', 'total', 'payment_method'
#         )
#         extra_kwargs = {'total': {'required': False}}
        
        
# class ReceiptSerializer(serializers.Serializer):
#     items = CartItemSerializer(many=True)
    
#     class Meta:
#         model = ShoppingSession  
#         fields = (
#             'id', 'shop', 'created_at', 'total', 'payment_method', 'items'
#         )

