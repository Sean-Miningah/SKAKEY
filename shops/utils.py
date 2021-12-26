from django.contrib.auth import authenticate
from rest_framework import serializers


def get_and_authenticate_shop(phonenumber, firebase_token):
    shop = authenticate(phonenumber=phonenumber, password=firebase_token)

    if shop is None:
        raise serializers.ValidationError(
            "Invalid username/password. Please try again!")

    return shop
