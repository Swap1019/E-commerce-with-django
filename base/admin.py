from django.contrib import admin
from .models import (
        TheProduct,
        PagePic,
        ProductCategory,
        Cart
    )
# Register your models here.

class TheProductAdmin(admin.ModelAdmin):
    list_display = ('product','pic_sample_preview','price','imported_at','availability','created_by')
    search_fields = ('product','tags')

class PagePicAdmin(admin.ModelAdmin):
    list_display = (['website_pic'])

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('parent','title','slug','status','position')
    list_filter = ('parent','title','status','position')
    search_fields = ('parent', 'title')
    ordering = ['-status']

class CartAdmin(admin.ModelAdmin):
    list_display = ('user','product','quantity')
    list_filter = ('user','product','quantity')
    search_fields = ('user','product')

admin.site.register(TheProduct,TheProductAdmin)
admin.site.register(PagePic,PagePicAdmin)
admin.site.register(ProductCategory,ProductCategoryAdmin)
admin.site.register(Cart,CartAdmin)

