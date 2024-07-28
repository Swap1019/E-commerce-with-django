from django.contrib import admin
from .models import (
        TheProduct,
        PagePic,
        ProductCategory,
        Cart,
        Images,
    )
# Register your models here.

class TheProductAdmin(admin.ModelAdmin):
    list_display = ('product','price','discount_percentage','created_at','quantity','availability','created_by','id')
    search_fields = ('product','tags','id')

class ImagesAdmin(admin.ModelAdmin):
    list_display = ('images_preview','product','id')
    search_fields = ('product','id')

class PagePicAdmin(admin.ModelAdmin):
    list_display = (['website_pic'])

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('parent','title','slug','status','position','id')
    list_filter = ('parent','title','status','position')
    search_fields = ('parent', 'title','id')
    ordering = ['-status']

class CartAdmin(admin.ModelAdmin):
    list_display = ('user','product','cart_product_price','quantity','total_cart_price','is_it_valid','id')
    list_filter = ('user','product','quantity')
    search_fields = ('user','product','id')

admin.site.register(TheProduct,TheProductAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(PagePic,PagePicAdmin)
admin.site.register(ProductCategory,ProductCategoryAdmin)
admin.site.register(Cart,CartAdmin)

