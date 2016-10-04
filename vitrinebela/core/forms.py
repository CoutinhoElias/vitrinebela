# coding=utf-8

from django import forms
from material import Fieldset
from material import Layout
from material import Row


class ContactForm(forms.Form):
    name = forms.CharField(label='Nome')
    email = forms.EmailField(label='E-Mail')
    message = forms.CharField(label='Mensagem', widget=forms.Textarea)

    layout = Layout(
        Fieldset('Cadastrar em SOS my PC',
                 'name', 'email',
                 Row('message')))
