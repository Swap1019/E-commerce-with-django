from django.contrib import admin
from .models import the_product,page_pic,product_category
from django.utils.html import mark_safe
# Register your models here.

class the_product_admin(admin.ModelAdmin):
    list_display = ('product','pic_sample_preview','price')
    search_fields = (['product'])

class page_pic_admin(admin.ModelAdmin):
    list_display = (['website_pic'])

class product_category_admin(admin.ModelAdmin):
    list_display = ('parent','title','slug','status','position')
    list_filter = ('parent','title','status','position')
    search_fields = ('parent', 'title')
    ordering = ['-status']

admin.site.register(the_product,the_product_admin)
admin.site.register(page_pic,page_pic_admin)
admin.site.register(product_category,product_category_admin)