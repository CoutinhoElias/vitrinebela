# coding=utf-8


from vitrinebela.catalog.models import Category


def categories(request):
    return {
        'categories': Category.objects.all()
    }
