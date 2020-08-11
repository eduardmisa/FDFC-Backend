from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from middleware.security import AllowAny
from django.shortcuts import render
from entities import models
from django.db.models import F, Q, Sum
from .serializers import *
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
import bcrypt


class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        firstname = serializer.validated_data.get('firstname')
        middlename = serializer.validated_data.get('middlename')
        lastname = serializer.validated_data.get('lastname')

        existing_username = models.User.objects.filter(username=username).first()
        if existing_username:
            return Response({"error": "Username Already Used"},
                            status=status.HTTP_401_UNAUTHORIZED,)

        existing_basic_details = models.User.objects.filter(firstname=firstname,lastname=lastname).first()
        if existing_basic_details:
            return Response({"error": "Basic details already registered"},
                            status=status.HTTP_401_UNAUTHORIZED,)

        new_user = models.User()
        new_user.username = username
        new_user.password = password
        new_user.firstname = firstname
        new_user.middlename = middlename
        new_user.lastname = lastname

        new_user.save()

        new_token = get_random_string(length=32)
        expires = datetime.now() + timedelta(hours=1)

        usersession = models.UserSession.objects.filter(user_id=new_user.id).first()
        if usersession:
            usersession.delete()
        models.UserSession(user=new_user,
                            token=new_token,
                            expires=expires).save()
        return Response({
            'token': new_token
        })


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        # Validate user access
        user = models.User.objects.filter(username=username).first()

        if not user:
            return Response("Invalid username or password",
                            status=status.HTTP_401_UNAUTHORIZED,)

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode()):
            return Response("Invalid username or password",
                            status=status.HTTP_401_UNAUTHORIZED,)

        new_token = get_random_string(length=32)
        expires = datetime.now() + timedelta(hours=1)

        usersession = models.UserSession.objects.filter(user_id=user.id).first()
        if usersession:
            usersession.delete()
        models.UserSession(user=user,
                            token=new_token,
                            expires=expires).save()
        return Response({
            'token': new_token
        })


class CurrentUserContext(APIView):
    
    def get(self, request, token=None, *args, **kwargs):
        serializer = CurrentUserContextSerializer
        serializer = serializer(request.user)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)


class Logout(APIView):
    def post(self, request, *args, **kwargs):
        return
        existingUser = self.request.user
        if existingUser:
            existingToken = Token.objects.filter(user=existingUser).first()
            if existingToken:
                existingToken.delete()
                return Response(data={"detail": "User was logged out"},
                                status=status.HTTP_200_OK)
            else:
                return Response(data={"detail": "User session not found"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data={"detail": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)
