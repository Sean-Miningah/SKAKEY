# import json
# from re import S
# from django.http import JsonResponse
# from django.core.exceptions import ObjectDoesNotExist
import random
from collections import namedtuple
from datetime import datetime
from django.utils.dateparse import parse_date

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view, permission_classes
# from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


from .models import (
    OTPAuthentication, Shop, County, SubCounty, Ward)
from .serializers import (
    OTPSerializer, ShopSerializer,ShopKeeperSerializer, 
    CountySerializer, SubCountySerializer,WardSerializer)

# from payment.serializers import PaymentMethodSerializer

# from payment.models import PaymentMethod
from django.contrib.auth import get_user_model
from .utilities import (get_and_authenticate_shopkeeper, rand_value,
                        otp_generator)
from shops.otp import SMS

ShopKeeper = get_user_model()

@api_view(['POST'])
def OTP_sms(request, id=False):
    otp_code = otp_generator()
    if not id:
        phone_number = request.data['phone_number']
        text_message = SMS().send(otp_code, [phone_number])
        res = {
            'OTP_CODE' : otp_code,
        }
    else:
        shop = Shop.objects.get(id=id)
        shopOwner = ShopKeeper.objects.get(shop=shop, is_owner=True)
        shop_phoneno=shopOwner.phone_number
        text_message = SMS().send(otp_code, [shop_phoneno])
        
        res = {
            'OTP_CODE': otp_code
        }
        
    return Response(res, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def OTP_response(request):
    phoneNumber = request.data['phone_number']
    randnumLength = 15
    try:
        authenticator = OTPAuthentication.objects.get(phone_number=phoneNumber)
        serializer = OTPSerializer(authenticator)
    except Exception as e:
        authenticator = OTPAuthentication(phone_number=phoneNumber,
                                    token=rand_value(randnumLength))
        authenticator.save()
        serializer = OTPSerializer(authenticator)
    finally:
        res = {
            'authentication_details' : serializer.data
        }

    return Response(res, status=status.HTTP_200_OK)


class CreateAccountView(viewsets.ModelViewSet):
    queryset = ShopKeeper.objects.all()
    serializer_class = ShopKeeperSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        shopkeeper = ShopKeeper.objects.get(phone_number=request.data['phone_number'])
        shopkeeper.set_password(request.data['login_token'])
        shopkeeper.save()
        token = Token.objects.create(user=shopkeeper)
        res = {
            "message": "Succesfully registered",
            "token": "Token " + token.key,
        }

        return Response(res, status=status.HTTP_201_CREATED, headers=headers)



class AccountInfoView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ShopKeeper.objects.all()
    serializer_class = ShopKeeperSerializer

    def list(self, request, *args, **kwargs):
        shopkeeper = request.user.id
        info = ShopKeeper.objects.get(id=shopkeeper)
        serializer = ShopKeeperSerializer(info)
        res = {
            "account-information": serializer.data
        }

        return Response(res, status=status.HTTP_201_CREATED)

class ShopView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Shop.objects.all()
    serializer_class =  ShopSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        #  Perform system checks of County -> Subcounty -> Ward before instance saving. 
        
        res = {
            "message" : "Shop Creation Succesfull",
        }
        
        return Response(res,status=status.HTTP_201_CREATED, headers=headers)


class LocationView(viewsets.ModelViewSet):
    def list(self, request):
        counties = County.objects.all()
        subcounties = SubCounty.objects.all()
        wards = Ward.objects.all()
        
        res = {
            "counties" : CountySerializer(counties, many=True).data,
            "subcounties": SubCountySerializer(subcounties, many=True).data,
            "wards": WardSerializer(wards, many=True).data    
        }
        
        return Response(res, status=status.HTTP_200_OK)
        
@api_view(['POST'])
def loginview(request):
    phone_number = request.data['phone_number']
    login_token = request.data['login_token']

    shopkeeper = get_and_authenticate_shopkeeper(phone_number, login_token)
    token = Token.objects.get(user=shopkeeper)
    
    res = {
        "message": "successfully logged in", 
        "token": "Token " + token.key
        }
    
    return Response(res, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def keeperassingment(request):
    id = request.data['id']
    try:
        shopkeeper = ShopKeeper.objects.get(id=request.user.id)
        shop = Shop.objects.get(id=id)
        shopkeeper.shop = shop
        shop.save()
        
        res = {
            "message": "User succesfully allocated to shop",
        }
    except Except as e:
        res = {
            "message": "The are no searched shops in the system."
        }
        
    return Response(res, status=status.HTTP_200_OK)
  
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))  
def RegisteredShopView(request):  
    shopkeeper_id = request.user.id
    
    shopkeeper = ShopKeeper.objects.get(id=shopkeeper_id)
    
    registered_shops = Shop.objects.get(id=shopkeeper.shop.id)
    
    serializer = ShopSerializer(registered_shops)
    
    res = {
        "Registered_shops": serializer.data,
    }
    
    return Response(res, status=status.HTTP_200_OK)
    
    
class LoginViewSet(viewsets.ModelViewSet):
    queryset = ShopKeeper.objects.all()
    serializer_class = ShopKeeperSerializer
    http_method_names = ['post', 'head']

    def create(self, request, *args, **kwargs):
        phone_number = request.data['phone_number']
        firebase_token = request.data['firebase_token']

        shopkeeper = get_and_authenticate_shopkeeper(phone_number, firebase_token)
        token = Token.objects.get(user=shopkeeper)
        res = {
            "message": "successfully logged in",
            "token": "Token " + token.key
        }

        return Response(res, status=status.HTTP_201_CREATED)


# class CategoryViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     # queryset = ProductCategory.objects.all()
#     serializer_class = ShopProductCategorySerializer
    
#     def get_queryset(self):
#         user = self.request.user
#         return ProductCategory.objects.filter(shop=user)

#     def create(self, request, *args, **kwargs):
#         request.data._mutable = True
#         request.data['shop'] = request.user.id
#         request.data._mutable = False
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)

#         res = {
#             "message": "Category Succesfully created"
#         }

#         return Response(res, status=status.HTTP_201_CREATED, headers=headers)


# class ProductViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     # queryset = ShopProduct.objects.all()
#     serializer_class = ShopProductSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['category']
    
#     def get_queryset(self):
#         user = self.request.user
#         return ShopProduct.objects.filter(shop=user)

#     def create(self, request, *args, **kwargs):
#         request.data._mutable = True
#         request.data['shop'] = request.user.id
#         print(request.data)
#         request.data._mutable = False
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         res = {
#             "message": "Product Succesfully created"
#         }

#         return Response(res, status=status.HTTP_201_CREATED, headers=headers)


# class CartViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = ShoppingSession.objects.all()
#     serializer_class = ShoppingSessionSerializer
    
#     def get_queryset(self):
#         user = self.request.user
#         return ShoppingSession.objects.filter(shop=user)

#     def create(self, request, *args, **kwargs):
#         # request.data._mutable = True
#         request.data['shop'] = request.user.id
#         # request.data._mutable = False
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)

#         res = {
#             "message": "cart_succesfully created",
#             "cart_id": serializer.instance.pk
#         }

#         return Response(res, status=status.HTTP_201_CREATED, headers=headers)
    
#     def partial_update(self, request, *args, **kwargs):
#         kwargs['partial'] = True
#         return self.update(request, *args, **kwargs)


# # class CartItemView(viewsets.ModelViewSet):
# #     permission_classes = [IsAuthenticated]
# #     queryset = CartItem.objects.all()
# #     serializer_class = CartItemSerializer

# #     def create(self, request, *args, **kwargs):
# #         data = request.data.copy()
# #         session = data['session']
# #         items = data.pop('items')
# #         this_session = ShoppingSession.objects.get(id=session)
# #         this_session.total = data["total"]
# #         this_session.save()
# #         # print(data)
# #         for item in items:
# #             item["session"] = this_session.id

# #         # print(items)
# #         print(items)
# #         serializer = self.get_serializer(
# #             data=items, many=isinstance(items, list))
# #         # print(serializer.is_valid())
# #         # serializer.is_valid(raise_exception=True)
# #         # if not serializer.is_valid():
# #         #     print(serializer.errors)
# #         print('\n')
# #         serializer.is_valid(raise_exception=True)
# #         self.perform_create(serializer)
# #         headers = self.get_success_headers(serializer.data)

# #         res = {
# #             "message": "Items created and added to cart"
# #         }

# #         return Response(res, status=status.HTTP_201_CREATED, headers=headers)


# # class CartItemViews(viewsets.ModelViewSet):
# #     permission_classes = [IsAuthenticated]
# #     queryset = CartItem.objects.all()
# #     serializer_class = CartItemSerializer

# #     def create(self, request):
# #         items = request.data.pop("items")
# #         this_session = request.data.pop("session")
# #         this_session = ShoppingSession.objects.get(id=this_session)

# #         this_session.total = request.data.pop("total")
# #         this_session.save()

# #         for item in items:
# #             print(item)
# #             print('\t \n \n')
# #             item["session"] = this_session.id
# #             item["shop_product"] = ShopProduct.objects.get(id=item["product"])
# #             CartItem.objects.create(session=this_session,
# #                                     product=item["shop_product"], quantity=item["quantity"], price=item["price"])

# #         res = {
#             "message": "Cart Item Created"
#         }

#         return Response(res, status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
# def cartsitem(request):
#     items = request.data.pop("items")
#     this_session = request.data.pop("session")
#     this_session = ShoppingSession.objects.get(id=this_session)
#     # payment_method = request.data.pop("payment_method")
#     # this_session.total = request.data.pop("total")
#     # this_session.save()
#     session_total = 0

#     for item in items:
#         item["shop_product"] = ShopProduct.objects.get(id=item["product"])
#         if item["shop_product"].quantity > item["quantity"]:
#             if (item["shop_product"].quantity - item["quantity"]) < 0:

#                 return Response({
#                     "message": "Product inventory is too low to satisfy this order"
#                 })
#             else:
#                 item["shop_product"].quantity = item["shop_product"].quantity - \
#                     item["quantity"]
#                 item["shop_product"].save()
#                 item["price"] = item["shop_product"].price * item["quantity"]
#                 session_total = session_total + item["price"]

#                 CartItem.objects.create(session=this_session,
#                                         product=item["shop_product"], quantity=item["quantity"], price=item["price"])
#         else:
#             return Response({
#                 "message": "Product inventory is too low to satisfy this order"
#             })

#     this_session.total = session_total
#     # this_session.payment_method = PaymentMethod.objects.get(id=payment_method)
#     this_session.save()

#     res = {
#         "message": "Cart Item(s) Created",
#         "session_total": this_session.total
#     }

#     return Response(res, status=status.HTTP_201_CREATED)

# # class InvoiceView(viewsets.ModelViewSet):
    
# #     def list(self, request):
# #         cart_id = request.data["cart_id"]
        
#         # shop = Shop.objects.get(id=request.user.id)
#         # cart = ShoppingSession.objects.get(id=cart_id)
#         # cart_items = CartItem.objects.filter(session=cart_id)
#         # paymentmethod = PaymentMethod.objects.get(id=cart.payment_method.id)
        
#         # # Invoice = namedtuple('Receipt',('shopname', 'cart', 'cartitems', 'paymentmethod'))
        
#         # # invoice = Invoice(
#         # #         shopname = shop,
#         # #         cart = cart, 
#         # #         cartitems = cart_items, 
#         # #         paymentmethod = paymentmethod
                
#         # #     )
        
#         # shop_info_serializer = ShopRegistrationSerializer(shop)
#         # cart_serializer = ShoppingSessionSerializer(cart)
#         # cart_items_serializer = CartItemSerializer(cart_items, many=True)
#         # payment_method_serializer = PaymentMethodSerializer(paymentmethod)     
#         # # serializer = ReceiptSerializer(Invoice)
        
#         # res = {
#         #     "shop_info" : shop_info_serializer.data,
#         #     "cart_info" : cart_serializer.data,
#         #     "cart_items": cart_items_serializer.data,
#         #     "payment_method": payment_method_serializer.data  
#         # }
        
#         # return Response(res, status=status.HTTP_200_OK)
    
# class SalesView(viewsets.ModelViewSet):
#     def list(self, request):
#         start_date = datetime.strptime(request.data["start_date"], '%Y-%m-%d').date()
#         end_date = datetime.strptime(request.data["end_date"], '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc)
        
#         # start_date = parse_date(request.data["start_date"])
#         # end_date = parse_date(request.data["end_date"])
        
#         carts= ShoppingSession.objects.filter(created_at=end_date,
#                                               shop=request.user.id)
#         print(f"This are the carts \n{carts}")
#         # cart_items = []
#         # for cart in carts:
#         #     # item = CartItem.objects.filter(session=cart.id)
#         #     # cart_items.append(item)
        
#         cart_serializer = ShoppingSessionSerializer(carts,many=True)
        
#         return Response(cart_serializer.data, status=status.HTTP_200_OK)
        
        