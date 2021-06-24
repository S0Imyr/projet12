from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    
    def __str__(self):
        return self.title


class User(AbstractUser):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(to=Role, on_delete=models.SET_NULL, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['last_name', 'email']

    def __str__(self):
        return self.username
