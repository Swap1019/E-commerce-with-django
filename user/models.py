from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
import uuid
# Create your models here.

class User(AbstractUser):
    is_seller = models.BooleanField(default=False,verbose_name='seller')
    user_id = models.UUIDField(default = uuid.uuid4,editable = False,unique=True)

class UserSellerInfo(models.Model):
    first_name = models.CharField(max_length=150,verbose_name="first name")
    last_name = models.CharField(max_length=150,verbose_name="last name")
    national_code = models.CharField(max_length=10,help_text="Your National Code must be 10 digits")
    identity_certificate = models.ImageField(upload_to='identity_certificate',verbose_name='identity certificate')
    user_id = models.UUIDField(default=None)

    def identity_view(self):
        return mark_safe(f'<img src = "{self.identity_certificate.url}" width = "120" height="120" style="border-radius: 5px"/>')
    identity_view.short_description = 'identity'

    