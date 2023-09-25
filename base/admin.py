from django.contrib import admin
from .models import the_product,page_pic,user_amount,time_amount
from django.utils.html import mark_safe
# Register your models here.

class the_product_admin(admin.ModelAdmin):
    list_display = ('product','pic_sample_preview')
    search_fields = (['product'])

class page_pic_admin(admin.ModelAdmin):
    list_display = (['website_pic'])

class user_amount_admin(admin.ModelAdmin):
    list_display = (['max_users'])

class time_amount_admin(admin.ModelAdmin):
    list_display = (['period'])

admin.site.register(the_product,the_product_admin)
admin.site.register(user_amount,user_amount_admin)
admin.site.register(time_amount,time_amount_admin)
admin.site.register(page_pic,page_pic_admin)