from django.shortcuts import render
from .forms import ContactForm

# Create your views here.


def index(request):
    return render(request, 'index.html')


def contact(request):
    form = ContactForm()
    context = {
        form: form
    }
    return render(request, 'contact.html', context)


# def product_list(request):
#     return render(request, 'product_list.html')


def product(request):
    return render(request, 'product.html')
