from django.contrib import admin
from imagekit.admin import AdminThumbnail
# Register your models here.
from.models import Product, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created', 'modified']
    search_fields = ['name', 'slug', 'created', 'modified']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'created', 'modified','__str__', 'admin_thumbnail']
    search_fields = ['name', 'slug', 'category__name', 'created', 'modified']
    admin_thumbnail = AdminThumbnail(image_field='smart')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
