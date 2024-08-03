from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
import uuid
# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(max_length=50,verbose_name="Nick Name",default='User')
    is_seller_status = (
                        ('N',"Not accepted"),
                        ('I',"Investigate"),
                        ('A',"Accepted")
                        )
    is_seller = models.CharField(default='N',max_length=1,choices=is_seller_status,verbose_name='seller')
    user_id = models.UUIDField(default = uuid.uuid4,editable = False,unique=True)
    profile = models.ImageField(upload_to="user_profile",blank=True,null=True)



class UserSellerInfo(models.Model):
    first_name = models.CharField(max_length=150,verbose_name="first name")
    last_name = models.CharField(max_length=150,verbose_name="last name")
    national_code = models.CharField(max_length=10,help_text="Your National Code must be 10 digits",unique=True)
    identity_certificate = models.ImageField(upload_to='identity_certificate',verbose_name='identity certificate')
    user_description = models.TextField(blank=True,help_text="Any descriptions (optional)")
    user_id = models.UUIDField(default=None,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    investigated = models.BooleanField(default=False)

    def identity_view(self):
        return mark_safe(f'<img src = "{self.identity_certificate.url}" width = "120" height="120" style="border-radius: 5px"/>')
    identity_view.short_description = 'identity'

class ReportedProduct(models.Model):
    reasons = (
        ('1',"NSFW"),
        ('2',"Fake Product"),
        ('3',"Scam"),
    )
    reported_product = models.ForeignKey('base.TheProduct',on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User,to_field='user_id',on_delete=models.CASCADE)
    reason = models.CharField(max_length=1,choices=reasons)
    explanation = models.TextField()
    checked = models.BooleanField(default=False,verbose_name='Investigated')

    def __str__(self):
        return self.reason
