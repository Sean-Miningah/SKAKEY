# import json
# from re import S
# from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import permission_classes
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


from .serializers import (
    ShopRegistrationSerializer,
    ShopProductCategorySerializer, ShopProductSerializer, ShoppingSession,
    CartItemSerializer,
    ShoppingSessionSerializer)
from .models import ProductCategory, ShopProduct, CartItem
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
    queryset = ShopProduct.objects.all()
    serializer_class = ShopProductSerializer

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['shop'] = request.user.id
        print(request.data)
        request.data._mutable = False
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(status=status.HTTP_201_CREATED, headers=headers)


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ShoppingSession.objects.all()
    serializer_class = ShoppingSessionSerializer

    def create(self, request, *args, **kwargs):
        # request.data._mutable = True
        request.data['shop'] = request.user.id
        # request.data._mutable = False
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        res = {
            "message": "cart_succesfully created",
            "cart_id": serializer.instance.pk
        }

        return Response(res, status=status.HTTP_201_CREATED, headers=headers)


# class CartItemView(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer

#     def create(self, request, *args, **kwargs):
#         data = request.data.copy()
#         session = data['session']
#         items = data.pop('items')
#         this_session = ShoppingSession.objects.get(id=session)
#         this_session.total = data["total"]
#         this_session.save()
#         # print(data)
#         for item in items:
#             item["session"] = this_session.id

#         # print(items)
#         print(items)
#         serializer = self.get_serializer(
#             data=items, many=isinstance(items, list))
#         # print(serializer.is_valid())
#         # serializer.is_valid(raise_exception=True)
#         # if not serializer.is_valid():
#         #     print(serializer.errors)
#         print('\n')
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)

#         res = {
#             "message": "Items created and added to cart"
#         }

#         return Response(res, status=status.HTTP_201_CREATED, headers=headers)


class CartItemViews(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def create(self, request):
        items = request.data.pop("items")
        this_session = request.data.pop("session")
        this_session = ShoppingSession.objects.get(id=this_session)

        this_session.total = request.data.pop("total")
        this_session.save()

        for item in items:
            item["session"] = this_session.id
            item["shop_product"] = ShopProduct.objects.get(id=item["product"])

        for item in items:
            CartItem.objects.create(session=this_session,
                                    product=item["shop_product"], quantity=item["quantity"], price=item["price"])

        res = {
            "message": "Cart Item Created"
        }

        return Response(res, status=status.HTTP_201_CREATED)
