from rest_framework import serializers
from entities import models
from datetime import datetime


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=15, required=True)
    password = serializers.CharField(max_length=50, required=True)
    firstname = serializers.CharField(max_length=255, required=True)
    middlename = serializers.CharField(max_length=255)
    lastname = serializers.CharField(max_length=255, required=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=50)


class CurrentUserContextSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    firstname = serializers.CharField(max_length=255)
    middlename = serializers.CharField(max_length=255)
    lastname = serializers.CharField(max_length=255)
