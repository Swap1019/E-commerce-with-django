from django.contrib import admin
from .models import the_product,page_pic
from django.utils.html import mark_safe
# Register your models here.

class the_product_admin(admin.ModelAdmin):
    list_display = ('product','pic_sample_preview','price')
    search_fields = (['product'])

class page_pic_admin(admin.ModelAdmin):
    list_display = (['website_pic'])

admin.site.register(the_product,the_product_admin)
admin.site.register(page_pic,page_pic_admin)