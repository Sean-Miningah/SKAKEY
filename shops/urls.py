from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register("create-shop", views.UserViewSet, basename="create-shop")
router.register("category", views.CategoryViewSet,
                basename="category")
router.register("shop-product", views.ProductViewSet, basename="shop-product")
router.register("login", views.LoginViewSet, basename="login")

router.register("cart", views.CartViewSet, basename="cart")
# router.register("cart-item", views.cartsitem, name='carts-item')

urlpatterns = [
    path('shop/', include(router.urls)),
    path('shop/cart-item/', views.cartsitem, name='carts-item'),
]
