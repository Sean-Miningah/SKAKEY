from rest_framework import serializers
# from rest_framework.authtoken import Token

from .models import (ProductCategory,
                     ShopProduct, ShoppingSession, CartItem)

from django.contrib.auth import get_user_model
Shop = get_user_model()

# Shop Serializer
###############################################


# class ShopLoginSerializer(serializers.Serializer):
#     phonenumber = serializers.CharField(max_length=300, required=True)
#     token = serializers.CharField(max_length=300,
#                                   required=True, write_only=True)


# class AuthShopSerializer(serializers.ModelSerializer):
#     auth_token = serializers.SerializerMethodField()

#     class Meta:
#         model = Shop
#         exclude = ['is_staff', 'is_active', 'start_date']

#     def get_auth_token(self, obj):
#         token = Token.objects.create(user=obj)
#         return token.key


# class EmptySerializer(serializers.Serializer):
#     pass

# class RegisterShopSerializer(serializers.ModelSerializer):


#############################################


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
            shop = Shop.objects.create(
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                shopname=validated_data["shopname"],
                location=validated_data["location"],
                photo=validated_data["photo"],
                category=validated_data["category"],
                firebase_token=validated_data["firebase_token"],
                phonenumber=validated_data["phonenumber"]
            )

            shop.set_password(validated_data["firebase_token"])
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


# class CartItemSerializer(serializers.ModelSerializer):
#     session = serializers.PrimaryKeyRelatedField(
#         queryset=ShoppingSession.objects.all, many=False)
#     product = serializers.PrimaryKeyRelatedField(
#         queryset=ShopProduct.objects.all(), many=False)

#     class Meta:
#         model = CartItem
#         fields = ['session', "product", "quantity", "price"]


# class ShoppingSessionSerializer(serializers.Serializer):
#     items = CartItemSerializer(many=True, read_only=False)
#     shop = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.all(),
#                                               many=False)
#     total = serializers.FloatField()

#     def create(self, validated_data):
#         # Creating the Session instance
#         shoppingsession = ShoppingSession.objects.create(shop=validated_data['shop'],
#                                                          total=validated_data['total'])

#         # Create the session items
#         for sesh_item in validated_data['items']:
#             items = CartItem(session=shoppingsession, product=sesh_item['product'],
#                              quantity=sesh_item['quantity'])
#             items.save()

#         return shoppingsession

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

    # def create(self, validated_data):
    #     #
    #     for item in validated_data:
    #         session = item["session"]
    #         sesh_obj = ShoppingSession.objects.get(id=session)
    #         CartItem.objects.create(session=sesh_obj, **item)

    #     return sesh_obj


class ShoppingSessionSerializer(serializers.ModelSerializer):
    # shop = serializers.PrimaryKeyRelatedField(
    #     queryset=Shop.objects.all(), many=False)
    # items = CartItemSerializer(many=True)

    # class Meta:
    #     model = ShoppingSession
    #     fields = (
    #         'id', 'shop', 'total', 'items'
    #     )

    # def create(self, validated_data):
    #     # Create Session
    #     session = ShoppingSession.objects.create()
    #     items_data = validated_data.pop('items')
    #     session = ShoppingSession.objects.create(**validated_data)
    #     print(session)
    #     for item_data in items_data:
    #         print(session)
    #         CartItem.objects.create(session=session, **item_data)
    #     return session

    shop = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.all(), many=False)

    class Meta:
        model = ShoppingSession
        fields = (
            'id', 'shop', 'created_at'
        )
        extra_kwargs = {'total': {'required': False}}
