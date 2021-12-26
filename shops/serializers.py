from rest_framework import serializers
# from rest_framework.authtoken import Token

from .models import ProductCategory, ShopProduct
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
