from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=128)
    allowed_control = models.BooleanField(default=False)
    ip_address = models.CharField(max_length=128)

    def __str__(self):
        return f'C-{self.ip_address}'
