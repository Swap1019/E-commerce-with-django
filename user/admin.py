from django.contrib import admin
from .models import User,UserSellerInfo,ReportedProduct

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','profile','first_name','last_name','is_staff','is_active','is_seller','user_id')

class UserSellerInfoAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','national_code','identity_view','user_id')
    search_fields = ('first_name','last_name','national_code','user_id')

class ReportedProductAdmin(admin.ModelAdmin):
    list_display = ('reported_product','checked','reason','user','explanation',)
    search_fields = ('reported_product','user','reason','checked')
    

admin.site.register(User,UserAdmin)
admin.site.register(UserSellerInfo,UserSellerInfoAdmin)
admin.site.register(ReportedProduct,ReportedProductAdmin)
