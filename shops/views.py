# import json
# from re import S
# from django.http import JsonResponse
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
        token = Token.objects.create(user=shop)
        res = {
            "message": "succesfully registered",
            "token": token.key
        }

        return Response(res, status=status.HTTP_201_CREATED, headers=headers)


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

        return Response(status=status.HTTP_201_CREATED, headers=headers)


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
