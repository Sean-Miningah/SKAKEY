# import json
# from re import S
# from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


from .serializers import (
    ShopRegistrationSerializer,
    ShopProductCategorySerializer, ShopProductSerializer)
from .models import ProductCategory, ShopProduct
from django.contrib.auth import get_user_model
from .utilities import get_and_authenticate_shop

Shop = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        shop = Shop.objects.get(phonenumber=request.data['phonenumber'])
        shop.set_password(request.data['firebase_token'])
        shop.save()
        token = Token.objects.create(user=shop)
        res = {
            "message": "succesfully registered",
            "token": "Token " + token.key
        }

        return Response(res, status=status.HTTP_201_CREATED, headers=headers)


class LoginViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopRegistrationSerializer
    http_method_names = ['post', 'head']

    def create(self, request, *args, **kwargs):
        phonenumber = request.data['phonenumber']
        firebase_token = request.data['firebase_token']

        shop = get_and_authenticate_shop(phonenumber, firebase_token)
        token = Token.objects.get(user=shop)
        res = {
            "message": "successfully logged in",
            "token": "Token " + token.key
        }

        return Response(res, status=status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ProductCategory.objects.all()
    serializer_class = ShopProductCategorySerializer

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['shop'] = request.user.id
        request.data._mutable = False
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        res = {
            "message": "Category Succesfully created"
        }

        return Response(res, status=status.HTTP_201_CREATED, headers=headers)


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ShopProduct
    serializer_class = ShopProductSerializer

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['shop'] = request.user.id
        request.data._mutable = False
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(status=status.HTTP_201_CREATED, headers=headers)
