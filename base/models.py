from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.html import mark_safe
from .limit import SingletonModel
from datetime import datetime,timedelta
from user.models import User
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.db.models import Count
from comment.models import Comment
from taggit.managers import TaggableManager

class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="ip_address")
    


class ProductCategory(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children',verbose_name="parent")
    title = models.CharField(max_length=200,verbose_name='Category-title')
    slug = models.SlugField(max_length=100,unique=True,verbose_name='Category-Addres')
    status = models.BooleanField(default=True, verbose_name='Make it publish')
    position = models.IntegerField(verbose_name='position')

    def __str__(self):
        return self.title
    

class TheProductManager(models.Manager):
    def availables(self,**kwargs):
        return super().get_queryset().filter(availability="A")
    
    def unavailables(self,**kwargs):
        return super().get_queryset().filter(availability="U")

    def new_arrivals(self,**kwargs):
        Today = datetime.today()
        last_week = Today-timedelta(days=7)
        return super().get_queryset().filter(imported_at__range=[last_week,Today],availability="A")
    
    def most_rated_products(self,**kwargs):
        return super().get_queryset().filter(ratings__isnull=False).order_by('-ratings__average')

    def most_viewed_products(self,**kwargs):
        return super().get_queryset().filter(availability="A").annotate(
            count=Count('hits')).order_by('-count')
        
class TheProduct(models.Model):
    product = models.CharField(max_length=50, verbose_name="product")
    period_choices = (
        ('1',"One_months"),
        ('3',"Three_months"),
        ('6',"Six_months"),
    )
    users = (
        ('1','One'),
        ('2','Two'),
        ('3','Three'),
        ('4','Four'),
        ('5','Five'),
    )
    status = (
        ('A','Available'),
        ('U','Unavailable'),
        ('I','Investigate'),
        ('B','Banned')
    )
    category = models.ManyToManyField(ProductCategory,verbose_name='Category',related_name="category")
    created_by = models.ForeignKey(User,to_field='user_id',on_delete=models.CASCADE,default=None,blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="price",default=50)
    discount_percentage = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    pic_sample = models.ImageField(upload_to="images", verbose_name='picture')
    description = models.TextField(verbose_name="description")
    period = models.CharField(max_length=1,choices=period_choices,verbose_name="period",default='1')
    max_users = models.CharField(max_length=1,choices=users,verbose_name="Users_in_same_time",default='1')
    imported_at = models.DateTimeField(auto_now_add=True,blank=True,verbose_name="imported_at")
    availability = models.CharField(max_length=1,choices=status,default='I',verbose_name='Status')
    hits = models.ManyToManyField(IPAddress,through="ProductHit", blank=True, related_name='hits',verbose_name='view_counts')
    tags = TaggableManager()
    ratings = GenericRelation(Rating, related_query_name='products')
    comments = GenericRelation(Comment)

    class ReadonlyMeta:
        readonly = ['final_price']

    def __str__(self):
        return self.product
    
    def category_names(self):
        return ', '.join([a.title for a in self.category.all()])
    category_names.short_description = "Admin Names"
    
    def pic_sample_preview(self):
        return mark_safe(f'<img src = "{self.pic_sample.url}" width = "120" height="120" style="border-radius: 5px"/>')
    pic_sample_preview.short_description = 'thumbnail'


    objects = TheProductManager()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(TheProduct,to_field='id',on_delete=models.CASCADE)
    cart_product_price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    total_cart_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)

    class ReadonlyMeta:
        readonly = ['total_cart_price']

    def __str__(self):
        return f"{self.quantity}"

class PagePic(SingletonModel):
    website_pic = models.ImageField(upload_to="images", verbose_name='website_pic')
    class Meta:
        verbose_name = 'website_pic'
        verbose_name_plural = 'website_pic'

class ProductHit(models.Model):
    product = models.ForeignKey(TheProduct, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    