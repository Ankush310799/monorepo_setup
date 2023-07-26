from django.db import models
from users.models import User


class Address(models.Model):
    street = models.CharField(max_length=200 , blank=False )
    city = models.CharField(max_length=100 , blank=False )
    state = models.CharField(max_length=100 , blank=False )
    country = models.CharField(max_length=100 , blank=False )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
