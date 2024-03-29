from django.utils import timezone
from django.db import models
from .modelcommon import BaseClass
from . import enums
# Create your models here.


class User(BaseClass):
    code = models.CharField(
        unique=True,
        null=False,
        max_length=10)
    username = models.CharField(
        unique=True,
        blank=False,
        null=False,
        max_length=15)
    password = models.CharField(
        unique=True,
        blank=False,
        null=False,
        max_length=255)
    password_salt = models.CharField(
        unique=True,
        blank=False,
        null=False,
        max_length=255)
    firstname = models.CharField(
        blank=False,
        null=False,
        max_length=100)
    middlename = models.CharField(
        null=True,
        blank=True,
        max_length=100)
    lastname = models.CharField(
        blank=False,
        null=False,
        max_length=100)
    birthdate = models.DateField(
        blank=False,
        null=False,
        default=timezone.now)

    is_active = models.BooleanField(
        default=True)
    is_administrator = models.BooleanField(
        default=False)

    def __str__(self):
        return f'{self.username}'

    class Meta:
            db_table = 'users'


class UserSession(BaseClass):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name='user_sessions')
    token = models.CharField(
        unique=True,
        max_length=255,
        blank=False,
        null=False)
    expires = models.DateTimeField()

    class Meta:
        db_table = 'user_sessions'


class FormState(BaseClass):
    code = models.CharField(
        unique=True,
        null=False,
        max_length=10)

    current_step = models.CharField(
        max_length=255,
        null=True,
        blank=True)

    firstname = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    middlename = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    lastname = models.CharField(
        max_length=255,
        null=True,
        blank=True)

    reference_number_1 = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    reference_number_2 = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    reference_number_3 = models.CharField(
        max_length=255,
        null=True,
        blank=True)

    tracking_number_1 = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    tracking_number_2 = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    tracking_number_3 = models.CharField(
        max_length=255,
        null=True,
        blank=True)

    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name='form_states')

    def __str__(self):
        return f'{self.username}'

    class Meta:
            db_table = 'form_states'