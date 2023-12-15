from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
import uuid
# Create your models here.

class UserManager(models.Manager):
    def New_Requests(self):
        return super.get_queryset().filter(is_seller="I")

class User(AbstractUser):
    nickname = models.CharField(max_length=50,verbose_name="Nick Name",default='User')
    is_seller_status = (
                        ('N','Not accepted'),
                        ('I','Investigate'),
                        ('A','Accepted')
                        )
    is_seller = models.CharField(default='N',max_length=1,choices=is_seller_status,verbose_name='seller')
    user_id = models.UUIDField(default = uuid.uuid4,editable = False,unique=True)
    profile = models.ImageField(upload_to="user_profile",blank=True,null=True)
    admin_reject_reason = models.TextField(default='Not reviewed yet')




    


class UserSellerInfo(models.Model):
    first_name = models.CharField(max_length=150,verbose_name="first name")
    last_name = models.CharField(max_length=150,verbose_name="last name")
    national_code = models.CharField(max_length=10,help_text="Your National Code must be 10 digits",unique=True)
    identity_certificate = models.ImageField(upload_to='identity_certificate',verbose_name='identity certificate')
    user_description = models.TextField(blank=True,help_text="Any descriptions (optional)")
    user_id = models.UUIDField(default=None,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def identity_view(self):
        return mark_safe(f'<img src = "{self.identity_certificate.url}" width = "120" height="120" style="border-radius: 5px"/>')
    identity_view.short_description = 'identity'

