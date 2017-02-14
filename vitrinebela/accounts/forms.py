# coding=utf-8

from django.contrib.auth.forms import UserCreationForm
from django import forms
from material import Fieldset
from material import Layout
from material import Row
from material import Span12
from material import Span6

from .models import User


class UserAdminCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email']
    layout = Layout(
        Span6('username'), Span6('email'),
        Row(Span6('password1'), Span6('password2')))


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'is_active', 'is_staff']

