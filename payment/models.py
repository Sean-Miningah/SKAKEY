from django.db import models


# Create your models here.

PAYMENT_CHOICES = (
    ('CASH', 'cash'),
    ('CREDIT','credit'),
    ('M-PESA','m-pese'),
    ('VOOMA', 'vooma') 
)

class PaymentMethod(models.Model):
    method = models.CharField(max_length=50,
                    default = 'CASH')

    def __str__(self):
        return self.method
    
class CreditPayment(models.Model):
    session = models.ForeignKey('shops.ShoppingSession', on_delete=models.PROTECT)
    name = models.CharField(max_length=50, default = 'none')
    number = models.CharField(max_length=15, blank=False)
    email  = models.CharField(max_length=40, blank=True)
    amount_payed = models.IntegerField(blank=False)
    total_shopping = models.IntegerField(blank=False)
    amount_remaining = models.IntegerField(blank=False)
    date_payment_expected = models.DateField(blank=False)
    last_update = models.DateField(auto_now=True)
    
    
    def __str__(self):
        return self.name
    