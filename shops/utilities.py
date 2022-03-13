from django.contrib.auth import authenticate
from rest_framework import serializers

import random
import string 
import secrets


def get_and_authenticate_shopkeeper(phone_number, login_token):
    shopkeeper = authenticate(phone_number=phone_number, password=login_token)

    if shopkeeper is None:
        raise serializers.ValidationError(
            "Invalid username/password. Please try again!")

    return shopkeeper



def rand_value(length):
    res = ''.join(secrets.choice(string.ascii_letters + 
                                 string.digits + string.punctuation)for x in range(length))
    
    return str(res)