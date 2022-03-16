from django.db import models
# from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

import random

# from datetime import date

# from payment.models import PaymentMethod

class OTPAuthentication(models.Model):
    token = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=40, unique=True)


class CustomAccountManager(BaseUserManager):

    def create_user(self, phone_number, password, **other_fields):
        if not phone_number:
            raise ValueError("A phone number must be provided")

        user = self.model(phone_number=phone_number, **other_fields)

        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, phone_number, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(phone_number, password, **other_fields)


class ShopKeeper(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    start_date = models.DateField(auto_now=True)
    phone_number = models.CharField(max_length=50, blank=False, unique=True)
    passportnumber = models.CharField(max_length=25, blank=True)
    is_owner = models.BooleanField(default=False)
    identity_no = models.CharField(max_length=50, blank=True)
    # login_token = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    shop = models.ForeignKey('Shop', related_name='shops',
                                   on_delete=models.RESTRICT, blank=True,
                                   null=True,default=None)
    
    objects = CustomAccountManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
class Shop(models.Model):
    name = models.CharField(max_length=20, blank=False,)
    confirmation_code = models.CharField(max_length=69, unique=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    start_date = models.DateField(auto_now=True)
    email_address = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(upload_to='user/shop/')
    category = models.CharField(max_length=20, blank=False)
    county = models.ForeignKey('County', related_name='county',
                               on_delete=models.RESTRICT, blank=True)
    
    device_id = models.CharField(max_length=100, blank=True)
    subcounty=models.ForeignKey('Subcounty', related_name='subcounty',
                                on_delete=models.RESTRICT, blank=True)
    
    ward=models.ForeignKey('Ward', related_name='ward', 
                           on_delete=models.RESTRICT, blank=True)
    
    
    def save(self, *args, **kwargs):
        self.confirmation_code = self.name[:2] + str(random.randint(100,1000))
        super(Shop, self).save(*args, **kwargs)
        
    # def regtoken(self):
    #     if not self.registration_id:
            
    #         registration_id = self.name + str(self.id + (10 ** 5))
    #         shop = Shop.objects.get(id=self.id)
    #         shop.registration_id = registration_id
    #         shop.save()
        
    def __str__(self):
        return self.name
    

class County(models.Model):
    name=models.CharField(max_length=20, blank=False, default='None')
    
    def __str__(self):
        return self.name
       

class SubCounty(models.Model):
    name=models.CharField(max_length=40, default="None",blank=False)
    county=models.ForeignKey('County', related_name="subcounty_county",
                             on_delete=models.CASCADE, blank=True)
    
    def __str__(self):
        return self.name
    
class Ward(models.Model):
    name=models.CharField(max_length=40, default="None", blank=False)
    subcounty=models.ForeignKey('SubCounty', related_name="subcounty_ward",
                             on_delete=models.CASCADE, blank=True)
    
    def __str__(self):
        return self.name
    

# class ProductCategory(models.Model):
#     # shop will be handled with session
#     shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
#     category = models.CharField(max_length=50, blank=False)
#     p_description = models.TextField(max_length=500, blank=False)
#     last_update = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.category


# class ShopProduct(models.Model):
#     shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50, blank=False)
#     quantity = models.IntegerField(editable=True)
#     price = models.BigIntegerField(editable=True)
#     p_description = models.TextField(max_length=250, blank=False)
#     category = models.ForeignKey(
#         ProductCategory, on_delete=models.CASCADE, blank=False)
#     source = models.CharField(max_length=50, blank=True)
#     date_created = models.DateTimeField(auto_now_add=True)
#     last_update = models.DateTimeField(auto_now=True)
#     photo = models.ImageField(upload_to='Shop/ShopProduct/', blank=True)
#     barcode = models.CharField(max_length=150, blank=True)
#     minimum_stock_level = models.BigIntegerField(editable=True, default=0)
#     reorder_quantity = models.IntegerField(editable=True, default=0)

#     def __str__(self):
#         return self.name

# # Shopping Cart Related Models


# class ShoppingSession(models.Model):
#     shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(default=timezone.now)
#     total = models.BigIntegerField(editable=True, null=True)
#     payment_method = models.ForeignKey(PaymentMethod, on_delete=models.RESTRICT, null=True)


# class CartItem(models.Model):
#     session = models.ForeignKey(
#         ShoppingSession, on_delete=models.CASCADE, blank=True)
#     product = models.ForeignKey(ShopProduct, on_delete=models.RESTRICT)
#     quantity = models.BigIntegerField(editable=True)
#     price = models.BigIntegerField(editable=True)

#     def __str__(self):
#         return str(self.product)


# class Invoice(models.Model):
#     session = models.ForeignKey(ShoppingSession, on_delete=models.RESTRICT)
#     shop = models.ForeignKey(Shop, on_delete=models.RESTRICT)
#     total = models.BigIntegerField(editable=True)
#     mode_of_payment = models.OneToOneField(
#         PaymentMethod, related_name="payment", on_delete=models.RESTRICT)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_update = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.created_at


# class OrderItem(models.Model):
#     invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
#     product = models.ForeignKey(
#         ShopProduct, on_delete=models.RESTRICT)
#     quantity = models.BigIntegerField(editable=True)
#     total_price = models.BigIntegerField(editable=True)
