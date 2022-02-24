from django.db import models
# from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# from datetime import date

# from payment.models import PaymentMethod


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
    is_employee = models.BooleanField(default=True)
    national_id = models.CharField(max_length=25, blank=True)
    firebase_token = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = CustomAccountManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
class Shop(models.Model):
    name = models.CharField(max_length=20, blank=False,)
    shopkeeper = models.ForeignKey('ShopKeeper', 
                                   on_delete=models.CASCADE, blank=True, default=None)
    latitude = models.FloatField()
    longitude = models.FloatField()
    start_date = models.DateField(auto_now=True)
    email_address = models.CharField(max_length=15, unique=True)
    photo = models.ImageField(upload_to='user/shop/')
    category = models.CharField(max_length=20, blank=False)
    county = models.ForeignKey('Shopkeeper', 
                               on_delete=models.CASCADE, blank=True, default=None)
    ward = models.CharField(max_length=100)
    subcounty=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class County(models.Model):
    name=models.CharField(max_length=20, blank=False, default='None')
       

class SubCounty(models.Model):
    name=models.CharField(max_length=40, default="None",blank=False)
    county=models.ForeignKey('County',
                             on_delete=models.CASCADE, blank=False)
    
class Ward(models.Model):
    name=models.CharField(max_length=30, default="None")
    county=models.ForeingKey('SubCounty', 
                             on_delete=models.CASCADE, blank=False)
    

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
