# from rest_framework import serializers 

# from payment.models import CreditPayment, PaymentMethod
# from shops.models import ShoppingSession 

# class PaymentMethodSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = PaymentMethod 
#         extra_kwargs = {"id":{"read_only":True},
#                         "method":{"read_only":True}}
#         fields = '__all__'

# class CreditPaymentSerializer(serializers.ModelSerializer):
    
#     session = serializers.PrimaryKeyRelatedField(
#         queryset=ShoppingSession.objects.all(), many=False)
    
#     class Meta:
#         model = CreditPayment
#         exclude = ['last_update']
        
        

