from middleware.current_user.data import get_current_user
from django.db import models
from datetime import datetime
from . import enums
import bcrypt

# Ordering of | null=True, blank=True | is IMPORTANT!:
#
# Order 1 : null=True, blank=True
#   NULL as default value
#
# Order 2 : blank=True, null=True
#   Requires to add 'default="your_default_val_here"
#   else, it will error upon saving

'''
BaseAuditClass
  The base class that will give:
  created, createdby, updated, updatedby, deleted & deletedby COLUMNS
  to whoever inehrits it.
'''

class BaseClass(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    createdby = models.CharField(max_length=255)
    modified = models.DateTimeField(auto_now=True)
    modifiedby = models.CharField(max_length=255)

    def save(self, *args, **kwargs):

        username = ""

        user = get_current_user()

        if user and user.username:
            username = user.username

        if self._state.adding:
            self.createdby = username
            self.modifiedby = username
        else:
            self.modifiedby = username

        if self._meta.object_name in enums.PrefixEnum.__members__:

            PREFIX = enums.PrefixEnum[self._meta.object_name].value

            willGenerateCode = (self.id == None and self.code == '')

            super().save(*args, **kwargs)

            if willGenerateCode:
                self.code = f'{PREFIX}-{self.id}'

                if self._meta.object_name == 'User':
                    self.password_salt = bcrypt.gensalt(12)
                    self.password = bcrypt.hashpw(self.password.encode('utf-8'), self.password_salt)

                    self.password_salt = self.password_salt.decode()
                    self.password = self.password.decode()

                self.save()
        else:
            super().save(*args, **kwargs)

    class Meta:
        abstract = True
