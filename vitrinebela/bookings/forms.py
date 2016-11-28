from django import forms
from django.contrib.auth.models import User

from material import Fieldset
from material import Layout
from material import Row
from material import Span10
from material import Span3
from material import Span5
from material import Span6
from material import Span8
from material import Span4



class BookingsForm(forms.Form):
    user = forms.ModelChoiceField(label="Pessoa",queryset=User.objects.all(),)
    allday = forms.BooleanField(label='Dia inteiro')
    # description = "DateField options"
    title = forms.CharField(label='Titulo do agendamento')
    start = forms.DateTimeField(label='Inicia em...')
    end = forms.DateTimeField(label='Termina em...')
    created_on = forms.DateTimeField(label='Criado em...')
    authorized = forms.BooleanField(label='Autorizado')
    editable = forms.BooleanField(label='Editavel')
    color = forms.ChoiceField(label='Cor', choices=(('red', 'red'),
                                       ('blue', 'blue'),
                                       ('green', 'green'),
                                       ('black', 'black')))
    backgroundColor = forms.ChoiceField(label='Cor de fundo.', choices=(('red', 'red'),
                                       ('blue', 'blue'),
                                       ('green', 'green'),
                                       ('black', 'black')))

    layout = Layout(
        Fieldset("Inclua uma agenda",
                 Row('user','title'),
                 Row('start','end', 'created_on'),
                 Row(Span6('color'), Span6('backgroundColor')),
                 Row(Span4('authorized'), Span4('editable'), Span4('allday'))
                 )
    )

# input_formats = ['%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
#  '%Y-%m-%d %H:%M',       # '2006-10-25 14:30'
#  '%Y-%m-%d',             # '2006-10-25'
#  '%m/%d/%Y %H:%M:%S',    # '10/25/2006 14:30:59'
#  '%m/%d/%Y %H:%M',       # '10/25/2006 14:30'
#  '%m/%d/%Y',             # '10/25/2006'
#  '%m/%d/%y %H:%M:%S',    # '10/25/06 14:30:59'
#  '%m/%d/%y %H:%M',       # '10/25/06 14:30'
#  '%m/%d/%y']             # '10/25/06'
