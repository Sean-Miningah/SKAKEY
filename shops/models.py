from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_user(self, phonenumber, password, **other_fields):
        if not phonenumber:
            raise ValueError("A phone number must be provided")

        user = self.model(phonenumber=phonenumber, **other_fields)

        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, phonenumber, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(phonenumber, password, **other_fields)


class Shop(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    shopname = models.CharField(max_length=20, blank=False)
    start_date = models.CharField(default=timezone.now, max_length=50)
    location = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=15, unique=True)
    photo = models.ImageField(upload_to='user/shop/')
    category = models.CharField(max_length=20, blank=False)
    firebase_token = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'phonenumber'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.shopname


class ProductCategory(models.Model):
    # shop will be handled with session
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, blank=False)
    p_description = models.CharField(max_length=100, blank=False)
    last_update = models.DateTimeField(auto_now=True)

    def __string__(self):
        return self.category


class ShopProduct(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)
    quantity = models.FloatField(editable=True)
    price = models.BigIntegerField(editable=True)
    p_description = models.TextField(max_length=250, blank=False)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, blank=False)
    source = models.CharField(max_length=50, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='Shop/ShopProduct/', blank=True)
    barcode = models.CharField(max_length=150, blank=True)

    def __string__(self):
        return self.name

# shop carting models.
