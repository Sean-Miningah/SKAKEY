from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import (CartItem, Shop,
                     ShopProduct, ShoppingSession, ProductCategory)

# Register your models here.


class ShopAdminConfig(UserAdmin):
    ordering = ('-start_date',)
    search_fields = ('name',)
    list_display = ('id','name', 'firebase_token',
                    'category', 'is_staff')

    fieldsets = (
        (None, {'fields': ('shopname', 'first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('category',
         'firebase_token', 'start_date', 'password')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('category', 'firebase_token',
                       'password1', 'password2', 'is_staff', 'is_active', 'is_superuser',
                       'county', 'ward', 'subcount', 'latitude', 'longitude'),
        }),
    )


class SessionAdminConfig(admin.ModelAdmin):
    ordering = ("-created_at",)
    search_fields = ('shop', 'total')
    list_display = ('id', 'shop', 'created_at', 'total', 'payment_method')

    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'shop', 'created_at', 'total', 'payment_method'
            ),
        }),
    )


class CartAdminConfig(admin.ModelAdmin):
    ordering = ("-session",)
    search_fields = ('session', 'quantity', 'price', 'product')
    list_display = ('id', 'session', 'product', 'quantity', 'price')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'session', 'product', 'quantity', 'price'
            ),
        }),
    )


class CategoryAdminConfig(admin.ModelAdmin):
    ordering = ("last_update",)
    search_fields = ('shop', 'category')
    list_display = ('id', 'shop', 'category')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'shop', 'category', 'p_description'
            ),
        }),
    )


class ProductAdminConfig(admin.ModelAdmin):
    ordering = ("-price",)
    search_fields = ('shop', 'price', 'category', 'source')
    list_display = ('id', 'name', 'shop', 'quantity', 'price',)

    fieldsets = (
        (None, {'fields': ('name', 'p_description', 'category', 'source',)}),
        ('Other Information', {
         'fields': ('shop', 'quantity', 'price',)}),
        ('Media', {'fields': ('photo', 'barcode',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'shop', 'name', 'quantity', 'price', 'p_description',
                'category', 'source', 'photo', 'barcode',
            ),
        }),
    )


admin.site.register(Shop, ShopAdminConfig)
admin.site.register(ShopProduct, ProductAdminConfig)
admin.site.register(ProductCategory, CategoryAdminConfig)
admin.site.register(ShoppingSession, SessionAdminConfig)
admin.site.register(CartItem, CartAdminConfig)
