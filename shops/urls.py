from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# from payment import views as p_views


router = DefaultRouter()
router.register("shopkeeper-info", views.ShopKeeperView, basename="shopkeeper-info")
router.register("shop-info", views.ShopView, basename="shop-info")
router.register("location-info", views.LocationView, basename="location-info")
# router.register("login", views.loginview, basename="login")

# router.register("category", views.CategoryViewSet,
#                 basename="category")
# router.register("shop-product", views.ProductViewSet, basename="shop-product")

# router.register("payment/credit-details", p_views.CreditPaymentView, basename="credit")

# router.register("cart", views.CartViewSet, basename="cart")
# router.register("cart-invoice", views.InvoiceView, basename="cart-invoice")
# router.register("sales", views.SalesView, basename="sales")
# router.register("cart-item", views.cartsitem, name='carts-item')

urlpatterns = [
    path('shop/', include(router.urls)),
    path('shop/login/', views.loginview, name='login')
    # path('shop/cart-item/', views.cartsitem, name='carts-item'),
    # path("shop/payment/payment-method/", p_views.payment_method, name="payment-method")
]
