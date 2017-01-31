from django.contrib import admin

# Register your models here.
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'email', 'is_staff', 'is_active', 'date_joined', 'image']
    search_fields = ['username', 'name', 'email', 'is_staff', 'is_active', 'date_joined', 'image']


admin.site.register(User, UserAdmin)