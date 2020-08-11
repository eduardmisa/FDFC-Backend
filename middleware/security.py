from middleware.current_user.data import set_current_user
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from rest_framework import permissions
from datetime import datetime, timedelta
from django.conf import settings
from entities import models


class AppTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate_credentials(self, key):

        user_session = models.UserSession.objects.filter(token=key).first()

        if not user_session:
            raise exceptions.AuthenticationFailed('Invalid token')

        if user_session.expires < datetime.now():
            raise exceptions.AuthenticationFailed('Token has expired')

        user_session.expires = datetime.now() + timedelta(hours=1)
        user_session.save()

        set_current_user(user_session.user)

        return (user_session.user,
                user_session)


class IsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        if not request.user:
            return False
        return True


class AllowAny(permissions.BasePermission):        

    def has_permission(self, request, view):
        return True
