# import json
# from re import S
# from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view, permission_classes
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
        res = {
            "message": "Product Succesfully created"
        }

        return Response(res, status=status.HTTP_201_CREATED, headers=headers)


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
            print(item)
            print('\t \n \n')
            item["session"] = this_session.id
            item["shop_product"] = ShopProduct.objects.get(id=item["product"])
            CartItem.objects.create(session=this_session,
                                    product=item["shop_product"], quantity=item["quantity"], price=item["price"])

        res = {
            "message": "Cart Item Created"
        }

        return Response(res, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def cartsitem(request):
    items = request.data.pop("items")
    this_session = request.data.pop("session")
    this_session = ShoppingSession.objects.get(id=this_session)

    # this_session.total = request.data.pop("total")
    # this_session.save()
    session_total = 0

    for item in items:
        item["shop_product"] = ShopProduct.objects.get(id=item["product"])
        if item["shop_product"].quantity > item["quantity"]:
            if (item["shop_product"].quantity - item["quantity"]) < 0:

                return Response({
                    "message": "Product inventory is too low to satisfy this order"
                })
            else:
                item["shop_product"].quantity = item["shop_product"].quantity - \
                    item["quantity"]
                item["shop_product"].save()
                item["price"] = item["shop_product"].price * item["quantity"]
                session_total = session_total + item["price"]

                CartItem.objects.create(session=this_session,
                                        product=item["shop_product"], quantity=item["quantity"], price=item["price"])
        else:
            return Response({
                "message": "Product inventory is too low to satisfy this order"
            })

    this_session.total = session_total
    this_session.save()

    res = {
        "message": "Cart Item Created",
        "session_total": this_session.total
    }

    return Response(res, status=status.HTTP_201_CREATED)
