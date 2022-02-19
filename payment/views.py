from payment.models import PaymentMethod, CreditPayment
from payment.serializers import CreditPaymentSerializer, PaymentMethodSerializer
from shops.models import ShoppingSession 
# from payment.serializers import -

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def payment_method(request):
    if request.method == 'GET':
        p_methods = PaymentMethod.objects.all()
        serializer = PaymentMethodSerializer(p_methods, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

class CreditPaymentView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CreditPayment.objects.all()
    serializer_class = CreditPaymentSerializer 
    
    def get_queryset(self):
        user = self.request.user
        shoppingsessions = ShoppingSession.objects.filter(shop=user)
        
        def shopsession(sessions = []):
            for Sesh in sessions:
                return Sesh.id
        
        return CreditPayment.objects.filter(session = shopsession(shoppingsessions))
    
    def create(self, request, *args, **kwargs):
        # request.GET = request.GET.copy()
        # request.GET['date_payment_expected'] = str(request.GET[''])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        res = {
            "message": "Details Successfully created"
        }
        
        return Response(res, status=status.HTTP_201_CREATED, headers=headers)
        
    

