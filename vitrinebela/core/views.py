from django.shortcuts import render
from .forms import ContactForm

from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth import get_user_model

#especificamente para carregar as urls antes, também impede o import circular
from django.core.urlresolvers import reverse_lazy
# from django.core.mail import send_mail
# from django.conf import settings


User = get_user_model()

def index(request):
    return render(request, 'index.html')


def contact(request):
    success = False
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.send_mail()
        success = True

    context = {
        'form': form,
        'success': success
    }
    return render(request, 'contact.html', context)


def product(request):
    return render(request, 'product.html')


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    model = User
    success_url = reverse_lazy('login')


register = RegisterView.as_view()