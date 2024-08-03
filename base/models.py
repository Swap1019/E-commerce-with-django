from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.html import mark_safe
from django.utils import timezone
from .limit import SingletonModel
from datetime import datetime,timedelta
from user.models import User
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.db.models import Count
from comment.models import Comment
from colorfield.fields import ColorField
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
        return super().get_queryset().filter(availability='A')
    
    def unavailables(self,**kwargs):
        return super().get_queryset().filter(availability='U')

    def new_arrivals(self,**kwargs):
        Today = datetime.today()
        last_week = Today-timedelta(days=7)
        return super().get_queryset().filter(created_at__range=[last_week,Today],availability='A')
    
    def most_rated_products(self,**kwargs):
        return super().get_queryset().filter(ratings__isnull=False).order_by('-ratings__average')

    def most_viewed_products(self,**kwargs):
        return super().get_queryset().filter(availability='A').annotate(
            count=Count('hits')).order_by('-count')
        
class TheProduct(models.Model):
    '''final_price is virtually generated'''
    '''discount_precentage has another check constraint for limiting it to 100 manually added in database'''
    product = models.CharField(max_length=50, verbose_name='product')
    status = (
        ('A','Available'),
        ('U','Unavailable'),
        ('I','Investigate'),
        ('B','Banned')
    )
    category = models.ManyToManyField(ProductCategory,verbose_name='Category',related_name='category')
    created_by = models.ForeignKey(User,to_field='user_id',on_delete=models.CASCADE,default=None,blank=False)
    price = models.DecimalField(max_digits=13, decimal_places=2,verbose_name='price',default=50)
    pic_sample = models.ImageField(upload_to='images/thumbnail',help_text='This picture will be shown to the user in list pages')
    discount_percentage = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],default=0)
    final_price = models.DecimalField(max_digits=13, decimal_places=2,null=True,blank=True)
    description = models.TextField(verbose_name='description')
    specs = models.JSONField(verbose_name='Specifications')
    created_at = models.DateTimeField(auto_now_add=True,blank=True,verbose_name='imported_at')
    quantity = models.PositiveIntegerField(default=5)
    sold_quantity = models.PositiveIntegerField(default=0)
    availability = models.CharField(max_length=1,choices=status,default='I',verbose_name='Status')
    hits = models.ManyToManyField(IPAddress,through='ProductHit', blank=True, related_name='hits',verbose_name='view_counts')
    tags = TaggableManager()
    ratings = GenericRelation(Rating, related_query_name='products')
    comments = GenericRelation(Comment)

    class ReadonlyMeta:
        readonly = ['final_price']

    def __str__(self):
        return self.product
    
    def pic_sample_preview(self):
        return mark_safe(f'<img src = "{self.pic_sample.url}" width = "120" height="120" style="border-radius: 5px"/>')
    pic_sample_preview.short_description = 'thumbnail'

    def category_names(self):
        return ', '.join([a.title for a in self.category.all()])
    category_names.short_description = 'Admin Names'

    def save(self,*args,**kwargs):
        self.quantity_check()
        super().save(*args,**kwargs)

    def quantity_check(self):
        if self.quantity <= 0:
            self.availability = 'U'


    objects = TheProductManager()

class Images(models.Model):
    product = models.ForeignKey(TheProduct,to_field='id',related_name='productimages',on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images', verbose_name='picture')

    def images_preview(self):
        return mark_safe(f'<img src = "{self.images.url}" width = "120" height="120" style="border-radius: 5px"/>')
    images_preview.short_description = 'Image of the product'

class Colors(models.Model):
    product = models.ForeignKey(TheProduct,to_field='id',related_name='productcolors',on_delete=models.CASCADE)
    color = ColorField(verbose_name='color')


class Cart(models.Model):
    #total_cart_price is virtually generated
    progress_status_choices = (
        ('00','Refuesed'),
        ('25','In process'),
        ('50','Preparation to ship'),
        ('75','In shipping progress'),
        ('100','Shipped'),
        )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(TheProduct,to_field='id',on_delete=models.CASCADE,related_name='carts')
    cart_product_price = models.IntegerField(default=1)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)],default=1)
    color = ColorField(verbose_name='color')
    total_cart_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    valid_until = models.DateTimeField()
    checkout = models.BooleanField(default=False)
    progress_status = models.CharField(default='25',max_length=3,choices=progress_status_choices)

    class ReadonlyMeta:
        readonly = ['total_cart_price']

    def __str__(self):
        return f"{self.quantity}"
    
    def save(self, *args, **kwargs):
        # Set valid_until to 2 hours from now if it's not already set
        if not self.valid_until:
            self.valid_until = timezone.now() + timedelta(hours=2)
        super().save(*args, **kwargs)

    def is_it_valid(self):
        if self.valid_until > timezone.now() or self.checkout == True:
            return True
        else:
            self.delete()

class PagePic(SingletonModel):
    website_pic = models.ImageField(upload_to="images", verbose_name='website_pic')
    class Meta:
        verbose_name = 'website_pic'
        verbose_name_plural = 'website_pic'

class ProductHit(models.Model):
    product = models.ForeignKey(TheProduct, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    