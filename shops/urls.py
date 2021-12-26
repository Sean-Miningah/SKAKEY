from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register("create-shop", views.UserViewSet, basename="create-shop")
router.register("category", views.CategoryViewSet,
                basename="category")
router.register("shop-product", views.ProductViewSet, basename="shop-product")


urlpatterns = [
    path('shop', include(router.urls)),
]
