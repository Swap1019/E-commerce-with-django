from django.contrib import admin
from .models import User,UserSellerInfo

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','is_staff','is_active','is_seller','user_id')

class UserSellerInfoAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','national_code','identity_view','user_id')
    search_fields = ('first_name','last_name','national_code','user_id')

admin.site.register(User,UserAdmin)
admin.site.register(UserSellerInfo,UserSellerInfoAdmin)
