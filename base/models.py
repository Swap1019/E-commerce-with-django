from django.db import models
from django.utils.html import mark_safe
from .limit import SingletonModel

class user_amount(models.Model):
    max_users = models.IntegerField(verbose_name="Users_in_same_time",default=1)

class time_amount(models.Model):
    period = models.IntegerField(verbose_name="period_based_on_month",default=1)

class the_product(models.Model):
    product = models.CharField(max_length=50, verbose_name="product")
    pic_sample = models.ImageField(upload_to="images", verbose_name='picture')
    description = models.TextField(verbose_name="description")
    users_amount = models.ManyToManyField(user_amount)
    time_limit = models.ManyToManyField(time_amount)
    base_price = models.DecimalField(max_digits=10, decimal_places=2,default=50)
    users_amount_prices = models.JSONField(default=dict) 
    time_limit_prices = models.JSONField(default=dict) 

    def __str__(self):
        return self.product
    
    def pic_sample_preview(self):
        return mark_safe(f'<img src = "{self.pic_sample.url}" width = "120" height="120" style="border-radius: 5px"/>')
    pic_sample_preview.short_description = 'thumbnail'


class page_pic(SingletonModel):
    website_pic = models.ImageField(upload_to="images", verbose_name='website_pic')
    class Meta:
        verbose_name = 'website_pic'
        verbose_name_plural = 'website_pic'
    