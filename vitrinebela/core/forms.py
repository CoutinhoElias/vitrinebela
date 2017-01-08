# coding=utf-8

from django import forms
from django.conf import settings
from material import Fieldset
from material import Layout
from material import Row
from django.core.mail import send_mail

import smtplib
from email.mime.text import MIMEText

from material import Span12
from material import Span6


class ContactForm(forms.Form):
    name = forms.CharField(label='Nome')
    email = forms.EmailField(label='E-Mail')
    message = forms.CharField(label='Mensagem', widget=forms.Textarea)

    layout = Layout(
        Fieldset("Fale Conosco",
                 Row(Span6('name'), Span6('email')),
                 Row(Span12('message'))))

    def send_mail(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        message = 'Nome: {0}\nE-Mail:{1}\n{2}'.format(name, email, message)
        send_mail('Contato do Elias Cabeção', message, settings.DEFAULT_FROM_EMAIL, [email])

        # msg = MIMEText('Email configurado com sucesso!')
        # msg['Subject'] = "Email enviado pelo python"
        # msg['From']    = "ffctex@gmail.com"
        # msg['To']      = "elias.fortaleza@alterdata.com.br"
        #
        # s = smtplib.SMTP('smtp.mailgun.org', 587)
        #
        # s.login('postmaster@vitrinebela.com.br', 'r3****f9')
        # s.sendmail(msg['From'], msg['To'], msg.as_string())
        # s.quit()