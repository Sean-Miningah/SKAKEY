from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import (ShopKeeper, Shop, 
                     County, SubCounty, Ward)

# Register your models here.


class ShopKeeperAdminConfig(UserAdmin):
    ordering = ('-start_date',)
    search_fields = ('first_name', 'last_name')
    list_display = ('id','first_name', 'last_name', 'firebase_token',
                    'phone_number', 'is_employee', 'is_staff')

    fieldsets = (
        (None, {'fields': ('phone_number', 'shopname', 'first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('firebase_token', 'national_id',
                                 'passportnumber','start_date', 'password')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'shopname', 'firebase_token',
                       'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('first_name', 'last_name', 'start_date', 'national_id', 'is_employee',
    #                    'phone_number', 'passportnumber','firebase_token', 
    #                    'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),
    #     }),
    # )
    
class ShopAdminConfig(admin.ModelAdmin):
    ordering = ('-start_date',)
    search_fields = ('name', 'shopkeeper')
    list_display = ('id','name', 'email_address',
                    'category', 'county')

    # fieldsets = (
    #     (None, {'fields': ('name', 'shopkeeper')
    #             }),
    #     ('Personal', {'fields': ('start_date',
    #      'photo', 'ward', 'subcounty'),
    #                   }),
    # )

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('name', 'shopkeeper',
    #                    'latitude', 'longitude', 'start_date', 'email_address', 'photo',
    #                    'category', 'ward', 'county', 'ward', 'subcounty'),
    #     }),
    # )

class CountyAdminConfig(admin.ModelAdmin):
    search_fields = ('name',)
    list_display= ('id', 'name')
    

class SubCountyAdminConfig(admin.ModelAdmin):
    search_fields = ('name', 'county')
    list_display= ('id', 'name', 'county')    
    
class WardAdminConfig(admin.ModelAdmin):
    search_fields = ('name', 'subcounty')
    list_display= ('id', 'name', 'subcounty')  
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'name', 'subcounty',
            ),
        }),
    )

# class SessionAdminConfig(admin.ModelAdmin):
#     ordering = ("-created_at",)
#     search_fields = ('shop', 'total')
#     list_display = ('id', 'shop', 'created_at', 'total', 'payment_method')

    
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': (
#                 'shop', 'created_at', 'total', 'payment_method'
#             ),
#         }),
#     )


# class CartAdminConfig(admin.ModelAdmin):
#     ordering = ("-session",)
#     search_fields = ('session', 'quantity', 'price', 'product')
#     list_display = ('id', 'session', 'product', 'quantity', 'price')

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': (
#                 'session', 'product', 'quantity', 'price'
#             ),
#         }),
#     )


# class CategoryAdminConfig(admin.ModelAdmin):
#     ordering = ("last_update",)
#     search_fields = ('shop', 'category')
#     list_display = ('id', 'shop', 'category')

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': (
#                 'shop', 'category', 'p_description'
#             ),
#         }),
#     )


# class ProductAdminConfig(admin.ModelAdmin):
#     ordering = ("-price",)
#     search_fields = ('shop', 'price', 'category', 'source')
#     list_display = ('id', 'name', 'shop', 'quantity', 'price',)

#     fieldsets = (
#         (None, {'fields': ('name', 'p_description', 'category', 'source',)}),
#         ('Other Information', {
#          'fields': ('shop', 'quantity', 'price',)}),
#         ('Media', {'fields': ('photo', 'barcode',)}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': (
#                 'shop', 'name', 'quantity', 'price', 'p_description',
#                 'category', 'source', 'photo', 'barcode',
#             ),
#         }),
#     )


admin.site.register(ShopKeeper, ShopKeeperAdminConfig)
admin.site.register(Shop, ShopAdminConfig)
admin.site.register(County, CountyAdminConfig)
admin.site.register(SubCounty, SubCountyAdminConfig)
admin.site.register(Ward, WardAdminConfig)
# admin.site.register(ShopProduct, ProductAdminConfig)
# admin.site.register(ProductCategory, CategoryAdminConfig)
# admin.site.register(ShoppingSession, SessionAdminConfig)
# admin.site.register(CartItem, CartAdminConfig)
