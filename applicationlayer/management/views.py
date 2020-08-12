from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from django.shortcuts import render
from entities import models
from .serializers import *
import copy
from django.utils.crypto import get_random_string
from middleware.security import AllowAny

'''
A Common Viewset
This can be used to quickly setup
CRUD operations for specific model/table.

usage:
1. inherit this class (CrudViewSet)
2. provide required Serializers for each CRUD Operation

note:
* queryset field will remain in super class
* inherit this viewset for general purpose enpoints only
  like a basic crud operations.
'''
class CrudViewSet(viewsets.ModelViewSet):
    list_serializer = None
    retrieve_serializer = None
    create_serializer = None
    update_serializer = None
    delete_serializer = None

    @action(detail=False,
            methods=['get'],
            url_path='count-all',
            name="Retrieves current total record count")
    def count_all(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        return Response({"count":queryset.count()})

    def list(self, request, *args, **kwargs):
        self.serializer_class = self.list_serializer
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = self.retrieve_serializer
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        self.serializer_class = self.create_serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        self.serializer_class = self.update_serializer
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        self.serializer_class = self.delete_serializer
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


'''
UserViewSet Viewset
This does not use Common Viewset
Operations in this Viewset are customized
and requires to implement viewsets.ModelViewSet itself.
'''
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

    @action(detail=True,
            methods=['post'],
            url_path='save-form-state',
            name="Save user form state")
    def get_by_user(self, request, pk=None):

        existing_form_state = models.FormState.objects.filter(
            user__id=pk).first()
        
        if existing_form_state:

            existing_form_state.current_step = request.data.get('current_step')
            existing_form_state.firstname = request.data.get('firstname')
            existing_form_state.middlename = request.data.get('middlename')
            existing_form_state.lastname = request.data.get('lastname')
            existing_form_state.reference_number_1 = request.data.get('reference_number_1')
            existing_form_state.reference_number_2 = request.data.get('reference_number_2')
            existing_form_state.reference_number_3 = request.data.get('reference_number_3')
            existing_form_state.tracking_number_1 = request.data.get('tracking_number_1')
            existing_form_state.tracking_number_2 = request.data.get('tracking_number_2')
            existing_form_state.tracking_number_3 = request.data.get('tracking_number_3')

            existing_form_state.save()

            return Response(FormStateRetrieveSerializer(existing_form_state).data,
                status=status.HTTP_200_OK)
        else:
            body = copy.deepcopy(request.data)
            body['user'] = request.user.id

            serializer = FormStateCreateSerializer(data=body)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


'''
FormStateViewSet Viewset
This inherits the CrudViewSet for 
centralization of crud operations.
'''
class FormStateViewSet(CrudViewSet):
    lookup_field = 'code'
    queryset = models.FormState.objects.all().order_by('-id')
    list_serializer = FormStateListSerializer
    retrieve_serializer = FormStateRetrieveSerializer
    create_serializer = FormStateCreateSerializer
    update_serializer = FormStateUpdateSerializer
    delete_serializer = FormStateDeleteSerializer

    @action(detail=False,
            methods=['get'],
            url_path='get-by-user',
            name="Get user form state")
    def get_by_user(self, request):

        userCode = self.request.query_params.get('userCode')
        if userCode :
            existing_form_state = models.FormState.objects.filter(user__code=userCode).first()
            if existing_form_state:
                return Response(self.retrieve_serializer(existing_form_state).data,
                                status=status.HTTP_200_OK,)
            else:
                return Response({"error": "User does not have any form state"},
                                status=status.HTTP_404_NOT_FOUND,)
        else:
            return Response({"error": "userCode nto provided"},
                            status=status.HTTP_404_NOT_FOUND,)

