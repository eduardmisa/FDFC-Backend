from rest_framework import serializers
from entities import models



# USER SERIALIZERS
# ...
# ...
class UserRetreiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = ['password', 'password_salt']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = ['password', 'password_salt']
        
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = ['created', 'modified', 'createdby', 'modifiedby', 'code', 'password_salt']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = ['created', 'modified', 'createdby', 'modifiedby', 'code', 'password_salt', 'password']


# FORM STATES SERIALIZERS
# ...
# ...
class FormStateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FormState
        fields = '__all__'

class FormStateRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FormState
        fields = '__all__'

class FormStateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FormState
        exclude = [
            'code',
            'created',
            'createdby',
            'modified',
            'modifiedby']

class FormStateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FormState
        exclude = [
            'code',
            'created',
            'createdby',
            'modified',
            'modifiedby']

class FormStateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FormState
        fields = '__all__'
