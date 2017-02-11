from django import forms
# from django.contrib.auth.models import User

from django.contrib.admin.widgets import FilteredSelectMultiple

from material import Fieldset
from material import Layout
from material import Row
from material import Span10
from material import Span3
from material import Span5
from material import Span6
from material import Span8
from material import Span4

from vitrinebela.accounts.models import User
from vitrinebela.bookings.models import Booking


class BookingsForm(forms.ModelForm):
    allday = forms.BooleanField(label='Dia inteiro', required=False)
    title = forms.CharField(label='Titulo do agendamento')
    start = forms.DateTimeField(label='Inicia em...')
    end = forms.DateTimeField(label='Termina em...')
    #created_on = forms.DateTimeField(label='Criado em...')
    authorized = forms.BooleanField(label='Autorizado', required=False)
    editable = forms.BooleanField(label='Editavel', required=False)
    # ABAIXO, CHOICES NO FORMS VAI TER UMALISTAGEM NO TEMPLATE
    color = forms.ChoiceField(label='Cor', choices=(('blue', 'blue'),
                                                    ('red', 'red'),
                                                    ('green', 'green'),
                                                    ('black', 'black')))
    overlap = forms.BooleanField(label='Sobrepor?', required=False)
    holiday = forms.BooleanField(label='Feriado?', required=False)
    participants = forms.ModelMultipleChoiceField(label='Participantes', queryset=User.objects.all(), widget=FilteredSelectMultiple("Participantes", is_stacked=False, attrs={'class':'material-ignore', 'multiple':'True'}))

    class Meta:
        model = Booking
        exclude = ['created_on']
        fields = '__all__'

    layout = Layout(
        Fieldset("Inclua uma agenda",
                 Row('title', ),
                 Row('start','end', 'color'),
                 Row(Span6('holiday'),Span6('authorized'), ),
                 Row(Span6('editable'), Span6('allday')),
                 Row('overlap'),
                 Row('participants')
                 )
    )


# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=30, label="Nome")
#     # email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#     # keep_logged = forms.BooleanField(required=False, label="Keep me logged in")



# input_formats = ['%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
#  '%Y-%m-%d %H:%M',       # '2006-10-25 14:30'
#  '%Y-%m-%d',             # '2006-10-25'
#  '%m/%d/%Y %H:%M:%S',    # '10/25/2006 14:30:59'
#  '%m/%d/%Y %H:%M',       # '10/25/2006 14:30'
#  '%m/%d/%Y',             # '10/25/2006'
#  '%m/%d/%y %H:%M:%S',    # '10/25/06 14:30:59'
#  '%m/%d/%y %H:%M',       # '10/25/06 14:30'
#  '%m/%d/%y']             # '10/25/06'

#COR DO BOTAO INLINE
# .grey.lighten-4 {
#     background-color: #786ec7 !important;
# }
