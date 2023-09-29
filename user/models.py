from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_seller = models.BooleanField(default=False,verbose_name='seller')