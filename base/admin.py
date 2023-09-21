from django.contrib import admin
from .models import the_product
# Register your models here.

class the_product_admin(admin.ModelAdmin):
    list_display = ('product','price','pic_sample_preview','period','max_users')
    list_filter = ('price','period','max_users')
    search_fields = (['product'])
    ordering = ['price']


admin.site.register(the_product,the_product_admin)