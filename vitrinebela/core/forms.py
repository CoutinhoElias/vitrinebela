# coding=utf-8

from django import forms
from django.conf import settings
from material import Fieldset
from material import Layout
from material import Row
from django.core.mail import send_mail


class ContactForm(forms.Form):
    name = forms.CharField(label='Nome')
    email = forms.EmailField(label='E-Mail')
    message = forms.CharField(label='Mensagem', widget=forms.Textarea)

    layout = Layout(
        Fieldset("Fale Conosco",
                 Row('name', 'email'),
                 Row('message')))

    def send_mail(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        message = 'Nome: {0}\nE-Mail:{1}\n{2}'.format(name, email, message)
        send_mail('Contato do Elias Fodão', message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
