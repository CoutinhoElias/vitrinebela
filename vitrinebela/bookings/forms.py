from django import forms
from material import Fieldset
from material import Layout
from material import Row
from material import Span3
from material import Span5
from material import Span8


class BookingsForm(forms.Form):
    title = forms.CharField(label='Titulo do agendamento')
    start = forms.DateTimeField(label='Inicia em...')
    end = forms.DateTimeField(label='Termina em...')
    created_on = forms.DateTimeField(label='Criado em...')
    authorized = forms.BooleanField(label='Autorizado')
    color = forms.ChoiceField(label='Cor')

    layout = Layout(
        Fieldset("Inclua uma agenda",
                 Row('title'),
                 Row('start','end', 'created_on'),
                 Row( Span8('authorized'), Span3('color')),
                 )
    )


CORES_CHOICES = (
    ('red', 'red'),
    ('blue', 'blue'),
    ('green', 'green'),
    ('black', 'black'),
)