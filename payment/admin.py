# from django.contrib import admin

# from payment.models import PaymentMethod,CreditPayment

# class PaymentMethodAdmin(admin.ModelAdmin):
#     list_display = ('id','method',)
#     search_fields = ['method']  
#     # exclude = ('id',)  
    
# class CreditPaymentAdmin(admin.ModelAdmin):
#     ordering =('-last_update',)
#     list_display = ('name', 'number', 'total_shopping', 'amount_remaining','amount_payed')
    
#     add_fieldsets = (
#         (None, {
#            'classes':('wide',),
#            'fields': (
#                'name', 'number', 'total_shopping', 'amount_remaining', 'amount_payed'
#            ) 
#         }),
#     )
# admin.site.register(PaymentMethod, PaymentMethodAdmin)
# admin.site.register(CreditPayment, CreditPaymentAdmin)
