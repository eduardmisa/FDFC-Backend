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
