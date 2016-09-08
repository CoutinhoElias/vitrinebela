# encode=utf-8

from django.shortcuts import render

# Create your views here.

from.models import Product


def produtct_list(request):
    context = {
        'product_list': Product.objects.all()
    }
    return render(request, 'catalog/product_list.html', context)
