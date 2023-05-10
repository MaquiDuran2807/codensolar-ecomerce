from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    telephone = models.IntegerField()
    password = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    codregistro = models.CharField(max_length=6, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email', 'telephone']
    objects = UserManager()
    
    def __str__(self):
        return self.name
