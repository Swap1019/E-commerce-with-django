from django.contrib import admin
from .models import User

# Register your models here.
class User_admin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','is_staff','is_active','is_seller')

admin.site.register(User,User_admin)
