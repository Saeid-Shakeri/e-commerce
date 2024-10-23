from django.db import models
from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=14,null=True,blank=True)
