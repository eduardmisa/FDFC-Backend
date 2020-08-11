from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from django.shortcuts import render
from entities import models
from .serializers import *
import copy
from django.utils.crypto import get_random_string
from middleware.security import AllowAny


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all().order_by('-created')
    serializer_class = UserCreateSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = UserListSerializer
        return super(UserViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = UserRetreiveSerializer
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = UserUpdateSerializer
        super(UserViewSet, self).update(request, *args, **kwargs)
        instance = models.User.objects.get(id=kwargs['pk'])
        serializer = UserRetreiveSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        self.serializer_class = UserCreateSerializer
        res = super(UserViewSet, self).create(request, *args, **kwargs)

        instance = models.User.objects.get(id=res.data['id'])
        serializer = UserRetreiveSerializer(instance)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,)


class FormStateViewSet(viewsets.ModelViewSet):
    queryset = models.FormState.objects.all().order_by('-created')
    serializer_class = UserCreateSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = UserListSerializer
        return super(UserViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = UserRetreiveSerializer
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = UserUpdateSerializer
        super(UserViewSet, self).update(request, *args, **kwargs)
        instance = models.FormState.objects.get(id=kwargs['pk'])
        serializer = UserRetreiveSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        self.serializer_class = UserCreateSerializer
        res = super(UserViewSet, self).create(request, *args, **kwargs)

        instance = models.FormState.objects.get(id=res.data['id'])
        serializer = UserRetreiveSerializer(instance)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,)