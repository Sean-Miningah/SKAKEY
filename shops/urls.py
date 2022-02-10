from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from payment import views as p_views


router = DefaultRouter()
router.register("create-shop", views.UserViewSet, basename="create-shop")
router.register("category", views.CategoryViewSet,
                basename="category")
router.register("shop-product", views.ProductViewSet, basename="shop-product")
router.register("login", views.LoginViewSet, basename="login")

router.register("payment/credit-details", p_views.CreditPaymentView, basename="credit")

router.register("cart", views.CartViewSet, basename="cart")
# router.register("cart-item", views.cartsitem, name='carts-item')

urlpatterns = [
    path('shop/', include(router.urls)),
    path('shop/cart-item/', views.cartsitem, name='carts-item'),
    path("shop/payment/payment-method/", p_views.payment_method, name="payment-method")
]
