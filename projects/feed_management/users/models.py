from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.conf import settings


class User(AbstractUser,PermissionsMixin):
    email = models.CharField(max_length=50,unique=True,null=True,blank=False)
    first_name = models.CharField(max_length=200,null=True,blank=False)
    last_name = models.CharField(max_length=200,null=True,blank=False)

    readonly_fields=('groups','user_permissions', )

    def __str__(self,):
        return self.username


class Group(models.Model):
    name = models.CharField(max_length=50,blank=False,null=False)

    def __str__(self,):
        return self.name
