from django.contrib import admin
from category.models import Tag, Category
# from forms import CategoryAdminForm


class TagAdmin(admin.ModelAdmin):
    """
    Tag Admin Class
    """
    list_display = ('name', 'slug', 'relevant', 'touched')
    fields = ('name', )


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin for Category
    """
    fields = ('name', )
    # form = CategoryAdminForm

# def _category(category):
#    return '<a href="%s">%s</a>' % (
#        reverse('admin:category_category_change',
# args=(category.category.id,)),
#        getattr(synonym.tag, _synonym_tag_name)
#    )

admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
