from django.contrib.auth import authenticate
from rest_framework import serializers


def get_and_authenticate_shop(phone_number, firebase_token):
    shopkeeper = authenticate(phone_number=phone_number, password=firebase_token)

    if shopkeeper is None:
        raise serializers.ValidationError(
            "Invalid username/password. Please try again!")

    return shopkeeper
