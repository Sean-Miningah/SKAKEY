from payment.models import Payment
# from payment.serializers import -

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

api_view(['GET',])
def payment_method(request):
    if request.method == 'GET':
        p_methods = Payment.objects.all()
        # serializers = 
