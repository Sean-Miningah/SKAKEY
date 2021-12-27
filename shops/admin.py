from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Shop, ShopProduct

# Register your models here.


class ShopAdminConfig(UserAdmin):
    ordering = ('-start_date',)
    search_fields = ('phonenumber', 'location', 'shopname')
    list_display = ('phonenumber', 'shopname', 'firebase_token',
                    'category', 'is_staff')

    fieldsets = (
        (None, {'fields': ('phonenumber', 'shopname', 'first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('category',
         'firebase_token', 'start_date', 'password')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phonenumber', 'location', 'firebase_token',
                       'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )


admin.site.register(Shop, ShopAdminConfig)
